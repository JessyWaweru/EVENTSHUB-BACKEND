import cloudscraper # <-- Back to using our Cloudflare bypass tool!
import time # <-- To add our "politeness" delay
from django.core.management.base import BaseCommand
from events.models import Event, User, Sponsor, Cinema, Showtime 
from django.utils import timezone

class Command(BaseCommand):
    help = 'Scrapes movies AND their full schedules stealthily from KenyaBuzz'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.WARNING("Starting Stealth Sync (Movies + Schedules)..."))

        movies_url = "https://api-v3.kenyabuzz.com/movies/now-showing-movies"
        schedules_url = "https://api-v3.kenyabuzz.com/schedule/cinema/fetch-shows"
        
        headers = {
            'sec-ch-ua-platform': '"iOS"',
            'Referer': 'https://www.kenyabuzz.com/',
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 18_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.5 Mobile/15E148 Safari/604.1',
            'Accept': 'application/json, text/plain, */*',
            'sec-ch-ua': '"Chromium";v="146", "Not-A.Brand";v="24", "Google Chrome";v="146"',
            'sec-ch-ua-mobile': '?1',
            'Content-Type': 'application/json'
        }

        # Initialize the stealth scraper
        scraper = cloudscraper.create_scraper(browser={'browser': 'chrome', 'platform': 'windows', 'desktop': True})

        try:
            # --- 1. PREP THE DATABASE ---
            admin_user = User.objects.filter(is_superuser=True).first()
            if not admin_user:
                self.stdout.write(self.style.ERROR("No superuser found! Run python manage.py createsuperuser"))
                return
                
            default_sponsor, _ = Sponsor.objects.get_or_create(
                title="KenyaBuzz", 
                defaults={"organisation": "KenyaBuzz", "category": "Entertainment", "industry": "Cinema"}
            )

            self.stdout.write("Clearing old showtimes from database...")
            Showtime.objects.all().delete()

            # --- 2. FETCH MOVIES ---
            self.stdout.write("Fetching Movies...")
            # We use scraper.get and increased timeout to 30!
            response = scraper.get(movies_url, headers=headers, timeout=30)
            response.raise_for_status() 
            movies_data = response.json()
            
            if isinstance(movies_data, list):
                movies_list = movies_data
            elif isinstance(movies_data, dict):
                movies_list = movies_data.get('data', [])
            else:
                movies_list = []

            # --- 3. LOOP MOVIES & FETCH SCHEDULES ---
            for movie_data in movies_list:
                if not isinstance(movie_data, dict):
                    continue

                title = movie_data.get('movie_name', 'Unknown Title')
                movie_slug = movie_data.get('movie_slug')
                image_url = movie_data.get('poster', '')
                rating = movie_data.get('rating', '18+')

                # Save the Event (Movie)
                event_obj, _ = Event.objects.update_or_create(
                    title=title, 
                    defaults={
                        'image': image_url,
                        'description': movie_data.get('synopsis', f"Catch {title} showing now!"),
                        'location': "Various Cinemas", 
                        'price': 850, 
                        'event_planner_name': 'KenyaBuzz Movies',
                        'event_planner_contact': '0700000000',
                        'age_limit': str(rating),
                        'capacity': 100,
                        'date': timezone.now(), 
                        'user': admin_user,
                        'sponsor': default_sponsor
                    }
                )

                if not movie_slug:
                    continue 

                # THE STEALTH DELAY: Wait 2 seconds before asking for schedules so we don't look like a bot spamming them
                time.sleep(2)

                # Fetch the Schedule for this specific movie
                payload = {"a": "m", "b": movie_slug, "c": False}
                
                try:
                    sched_res = scraper.post(schedules_url, headers=headers, json=payload, timeout=30)
                    if sched_res.status_code != 200:
                        continue
                except Exception as e:
                    print(f"⚠️ Network timeout on {title}, skipping schedules and moving to next...")
                    continue

                schedule_data = sched_res.json()
                cinemas_list = schedule_data.get('data', [])

                if not isinstance(cinemas_list, list):
                    print(f"⚠️ Skipped Showtimes for: {title} (No schedules available)")
                    continue

                showtimes_created = 0

                # --- 4. EXTRACT CINEMAS & SHOWTIMES ---
                for cinema_item in cinemas_list:
                    if not isinstance(cinema_item, dict):
                        continue

                    cin_info = cinema_item.get('cinema', {})
                    cinema_name = cin_info.get('cinema_name', 'Unknown Cinema').strip()
                    
                    cinema_obj, _ = Cinema.objects.get_or_create(
                        name=cinema_name,
                        defaults={'location': cin_info.get('cinema_address', 'Nairobi')}
                    )

                    for date_item in cinema_item.get('dates', []):
                        if not isinstance(date_item, dict):
                            continue
                        
                        m_date = date_item.get('movie_date')
                        
                        for m_data in date_item.get('movies', []):
                            if not isinstance(m_data, dict):
                                continue
                                
                            for show in m_data.get('shows', []):
                                if not isinstance(show, dict):
                                    continue
                                    
                                m_time = show.get('movie_time')
                                
                                if m_date and m_time:
                                    Showtime.objects.create(
                                        movie=event_obj,
                                        cinema=cinema_obj,
                                        date=m_date,
                                        time=m_time
                                    )
                                    showtimes_created += 1

                print(f"✅ Synced: {title} ({showtimes_created} showtimes found)")

            self.stdout.write(self.style.SUCCESS("\n🎉 SUCCESS! Your database is now fully synced with real-time cinemas and schedules!"))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Script failed: {e}"))