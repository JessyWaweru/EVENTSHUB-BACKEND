from rest_framework import serializers
from .models import User, Sponsor, Event, Speaker, Attendee

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

class EventSerializer(serializers.ModelSerializer):
    # If you want nested data (e.g., seeing speaker details inside the event), 
    # you can uncomment the lines below:
    # speakers = SpeakerSerializer(many=True, read_only=True)
    # sponsor = SponsorSerializer(read_only=True)

    class Meta:
        model = Event
        fields = '__all__'