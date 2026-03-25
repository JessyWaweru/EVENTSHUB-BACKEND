from rest_framework import serializers
from .models import User, Sponsor, Event, Speaker, Attendee, Cinema, Showtime


# ===========================
# MODEL SERIALIZERS
# ===========================
# The previous authentication-related serializers (UserRegistrationSerializer,
# LoginRequestSerializer, etc.) have been removed as Clerk now handles
# user registration and login on the frontend.

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'age', 'gender', 'created_at']
        # Exclude password_digest from the API response for security

class SponsorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sponsor
        fields = '__all__'

class SpeakerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Speaker
        fields = '__all__'

class AttendeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendee
        fields = '__all__'

# --- NEW SERIALIZERS FOR SCHEDULES ---

class CinemaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cinema
        fields = '__all__'

class ShowtimeSerializer(serializers.ModelSerializer):
    # This nests the full cinema details inside the showtime
    # so React gets the cinema name and location without doing extra API calls!
    cinema = CinemaSerializer(read_only=True) 

    class Meta:
        model = Showtime
        fields = ['id', 'date', 'time', 'ticket_link', 'cinema']

# -------------------------------------

class EventSerializer(serializers.ModelSerializer):
    # This automatically grabs all showtimes linked to this movie 
    # (using the related_name='showtimes' we set in models.py)
    showtimes = ShowtimeSerializer(many=True, read_only=True)
    
    # Optional: If you want to see sponsor details nested, uncomment this:
    # sponsor = SponsorSerializer(read_only=True)

    class Meta:
        model = Event
        fields = '__all__'