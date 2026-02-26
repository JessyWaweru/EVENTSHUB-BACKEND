from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    UserViewSet, SponsorViewSet, EventViewSet, SpeakerViewSet, AttendeeViewSet
)

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'sponsors', SponsorViewSet)
router.register(r'events', EventViewSet)
router.register(r'speakers', SpeakerViewSet)
router.register(r'attendees', AttendeeViewSet)

# The API URLs for the viewsets are now determined automatically by the router.
# The old authentication endpoints have been removed as Clerk now handles authentication.
urlpatterns = [
    # All CRUD endpoints are now under the router.
    # e.g., /api/users/, /api/events/, etc.
    path('', include(router.urls)),
]