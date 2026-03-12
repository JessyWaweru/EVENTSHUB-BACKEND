from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from .models import User, Sponsor, Event, Speaker, Attendee
from .serializers import (
    UserSerializer, SponsorSerializer, EventSerializer, 
    SpeakerSerializer, AttendeeSerializer
)
import requests
from bs4 import BeautifulSoup
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    # This is the magic line! Guests can view (GET), but only logged-in users can create/edit (POST, PUT, DELETE)
    permission_classes = [IsAuthenticatedOrReadOnly]

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    # Explicitly lock down the other endpoints
    permission_classes = [IsAuthenticated]

class SponsorViewSet(viewsets.ModelViewSet):
    queryset = Sponsor.objects.all()
    serializer_class = SponsorSerializer
    permission_classes = [IsAuthenticated]

class SpeakerViewSet(viewsets.ModelViewSet):
    queryset = Speaker.objects.all()
    serializer_class = SpeakerSerializer
    permission_classes = [IsAuthenticated]

class AttendeeViewSet(viewsets.ModelViewSet):
    queryset = Attendee.objects.all()
    serializer_class = AttendeeSerializer
    permission_classes = [IsAuthenticated]

class KenyaBuzzMoviesView(APIView):
    # This ensures anyone can view the movie times without logging in
    permission_classes = [AllowAny]

    def get(self, request):
        url = "https://www.kenyabuzz.com/movies"
        # We use a headers dictionary to mimic a real browser, otherwise some sites block the request!
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }
        
        movies_data = []

        try:
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            
            # Parse the HTML with BeautifulSoup
            soup = BeautifulSoup(response.content, 'html.parser')

            # =========================================================
            # NOTE: HTML structure changes! You must inspect the live 
            # KenyaBuzz website to get the exact class names.
            # Replace 'movie-item-class-here' with their actual wrapper class.
            # =========================================================
            movie_cards = soup.find_all('div', class_='movie-item-class-here') 

            for idx, card in enumerate(movie_cards[:15]): # Limit to top 15 to keep it fast
                try:
                    # Extract Title (Update the tag/class)
                    title_elem = card.find('h3', class_='title-class')
                    title = title_elem.text.strip() if title_elem else f"Movie {idx + 1}"

                    # Extract Image (Update the tag/class)
                    img_elem = card.find('img')
                    image = img_elem['src'] if img_elem and 'src' in img_elem.attrs else "https://via.placeholder.com/400x600?text=No+Poster"

                    # Extract Cinema Location (Update the tag/class)
                    cinema_elem = card.find('span', class_='location-class')
                    cinema = cinema_elem.text.strip() if cinema_elem else "Multiple Cinemas"

                    # Extract Showtimes (Update the tag/class)
                    time_elems = card.find_all('span', class_='time-class')
                    showtimes = [time.text.strip() for time in time_elems] if time_elems else ["Check Cinema"]

                    movies_data.append({
                        "id": str(idx),
                        "title": title,
                        "posterImage": image,
                        "cinema": cinema,
                        "genre": "Currently Showing", # Hard to scrape genres reliably, default string
                        "duration": "N/A",
                        "showtimes": showtimes
                    })
                except Exception as e:
                    print(f"Error parsing a movie card: {e}")
                    continue
            
            # FALLBACK: If the scraper found nothing (meaning the HTML classes need updating)
            # return some dummy data so your React frontend still renders beautifully.
            if not movies_data:
                movies_data = [
                    {
                        "id": "1", "title": "Dune: Part Two (Fallback Data)", 
                        "posterImage": "https://images.unsplash.com/photo-1536440136628-849c177e76a1?w=800&q=80", 
                        "cinema": "Century Cinemax - Sarit", "genre": "Sci-Fi", "duration": "2h 46m", 
                        "showtimes": ["11:00 AM", "2:30 PM", "6:00 PM"]
                    }
                ]

            return Response(movies_data)

        except requests.exceptions.RequestException as e:
            return Response({"error": f"Failed to fetch data from KenyaBuzz: {str(e)}"}, status=500)
