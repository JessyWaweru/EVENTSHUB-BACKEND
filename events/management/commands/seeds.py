from django.core.management.base import BaseCommand
from datetime import timezone
from faker import Faker
from events.models import User, Sponsor, Event, Speaker, Attendee

class Command(BaseCommand):
    help = 'Seeds the database with initial data'

    def handle(self, *args, **kwargs):
        self.stdout.write('Seeding database...')
        
        fake = Faker()

        # Delete existing data
        Attendee.objects.all().delete()
        Speaker.objects.all().delete()
        Event.objects.all().delete()
        Sponsor.objects.all().delete()
        User.objects.all().delete()

        # Create user
        user = User.objects.create_user(
            username="user",
            email="user@mail.com",
            password="password",
            gender="Female",
            age=18
        )

        # Create sponsors
        sponsor1 = Sponsor.objects.create(title="Google", organisation="Google Inc.", category="Technology", industry="Software")
        sponsor2 = Sponsor.objects.create(title="Nike", organisation="Nike Inc.", category="Fashion", industry="Sportswear")
        sponsor3 = Sponsor.objects.create(title="Coca-Cola", organisation="The Coca-Cola Company", category="Food and Beverage", industry="Beverages")

        # Create events
        events_data = [
            {
                "price": 1200, "event_planner_name": 'Jessica Pear', "event_planner_contact": '0703263352',
                "title": "Autism foundation", "image": "https://w0.peakpx.com/wallpaper/608/924/HD-wallpaper-autism-speaks-awareness-purple-april-puzzle-asd-autism.jpg",
                "description": "We take a look at how we have come in our knowledge and understanding of Autism",
                "location": "Sabaki", "age_limit": "All ages", "capacity": 5000, "date": fake.date_time_between(start_date='now', end_date='+50d', tzinfo=timezone.utc)
            },
            {
                "price": 2000, "event_planner_name": 'Jess Pear', "event_planner_contact": '0777263352',
                "title": "Music Festival", "image": "https://images.pexels.com/photos/2263436/pexels-photo-2263436.jpeg",
                "description": "Join us for a day of music, food, and fun!",
                "location": "Vasha", "age_limit": "22+", "capacity": 5000, "date": fake.date_time_between(start_date='now', end_date='+5d', tzinfo=timezone.utc)
            },
            {
                "price": 1000, "event_planner_name": 'Jessica Pear', "event_planner_contact": '0703263352',
                "title": "Charity Walk", "image": "https://media.istockphoto.com/id/1139537240/photo/african-american-woman-with-group-in-breast-cancer-rally.jpg",
                "description": "Join us for a charity walk to raise funds for cancer research.",
                "location": "From Nairobi CBD till Kitengela via the expressway", "age_limit": "15+", "capacity": 5000, "date": fake.date_time_between(start_date='now', end_date='+50d', tzinfo=timezone.utc)
            },
            # Keeping it concise for the snippet, but you can copy/paste the rest of your event dictionaries here following the same structure!
        ]

        # Saving events
        created_events = []
        for e_data in events_data:
            event = Event.objects.create(
                user=user,
                sponsor=sponsor2,
                **e_data
            )
            created_events.append(event)

        # Note: If your Speakers/Attendees depend on specific IDs, you can reference `created_events[0]` for Event 1, `created_events[1]` for Event 2, etc.

        # Create Speakers
        Speaker.objects.create(
            name="Stephen Hawking", email="stephen.h@speaker.com", event=created_events[0],
            organisation="STEPHEN HAWKING FOUNDATION", job_title="Founding Father", image="base64_string_here"
        )
        Speaker.objects.create(
            name="Bien", email="Bien@speaker.com", event=created_events[1],
            organisation="SAUTI SOL", job_title="Musician", image="base64_string_here"
        )
        Speaker.objects.create(
            name="Uhuru Kenyatta", email="kenyatta@speaker.com", event=created_events[2],
            organisation="CHARITY FOUNDATION", job_title="CEO", image="base64_string_here"
        )

        # Create Attendees (Simulating other users since the schema requested user_ids 2 and 3)
        user2 = User.objects.create_user(username="david", email="david@mail.com", password="password", age=25, gender="Male")
        user3 = User.objects.create_user(username="jenny", email="jenny@mail.com", password="password", age=22, gender="Female")

        Attendee.objects.create(name="Samantha Lee", email="samanthalee@example.com", user=user, event=created_events[2])
        Attendee.objects.create(name="David Kim", email="davidkim@example.com", user=user2, event=created_events[0])
        Attendee.objects.create(name="Jennifer Chen", email="jenniferchen@example.com", user=user3, event=created_events[2])

        self.stdout.write(self.style.SUCCESS('Successfully seeded the database!'))