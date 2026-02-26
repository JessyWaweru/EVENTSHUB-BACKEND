from rest_framework import viewsets
from .models import User, Sponsor, Event, Speaker, Attendee
from .serializers import (
    UserSerializer, SponsorSerializer, EventSerializer, 
    SpeakerSerializer, AttendeeSerializer
)

# With Clerk authentication now set as the default, all authentication logic
# (registration, login, token verification) is handled by the ClerkAuthentication class.
# The views below are standard ModelViewSets for CRUD operations.
# Access to these views is now protected by Clerk JWTs by default.

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class SponsorViewSet(viewsets.ModelViewSet):
    queryset = Sponsor.objects.all()
    serializer_class = SponsorSerializer

class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

class SpeakerViewSet(viewsets.ModelViewSet):
    queryset = Speaker.objects.all()
    serializer_class = SpeakerSerializer

class AttendeeViewSet(viewsets.ModelViewSet):
    queryset = Attendee.objects.all()
    serializer_class = AttendeeSerializer