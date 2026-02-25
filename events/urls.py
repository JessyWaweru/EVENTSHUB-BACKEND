from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    UserViewSet, SponsorViewSet, EventViewSet, SpeakerViewSet, AttendeeViewSet,
    RegisterView, VerifyEmailView, LoginView, PasswordResetRequestView, PasswordResetConfirmView
)

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'sponsors', SponsorViewSet)
router.register(r'events', EventViewSet)
router.register(r'speakers', SpeakerViewSet)
router.register(r'attendees', AttendeeViewSet)

# The API URLs are now determined automatically by the router.
urlpatterns = [
     # --- Auth Endpoints ---
    path('auth/register/', RegisterView.as_view(), name='auth_register'),
    path('auth/verify-email/', VerifyEmailView.as_view(), name='auth_verify'),
    path('auth/login/', LoginView.as_view(), name='auth_login'),
    
    # --- Password Reset ---
    path('auth/password-reset/', PasswordResetRequestView.as_view(), name='password_reset_request'),
    path('auth/password-reset/confirm/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),

    path('', include(router.urls)),
]