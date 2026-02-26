from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
import random
import datetime

class User(AbstractUser):
    email = models.EmailField(unique=True)
    age = models.IntegerField(null=True, blank=True)
    gender = models.CharField(max_length=20, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    admin = models.BooleanField(default=False)
    is_email_verified = models.BooleanField(default=False)
    clerk_user_id = models.CharField(max_length=255, unique=True, null=True, blank=True)

    def __str__(self):
        return self.username

    # The generate_otp and verify_otp methods have been removed as they were
    # part of the previous email/OTP authentication system. Clerk now handles this.


class Sponsor(models.Model):
    title = models.CharField(max_length=255)
    organisation = models.CharField(max_length=255)
    category = models.CharField(max_length=255)
    industry = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Event(models.Model):
    title = models.CharField(max_length=255)
    image = models.TextField() # Used TextField to accommodate long Base64 strings
    description = models.TextField()
    location = models.CharField(max_length=255)
    age_limit = models.CharField(max_length=50)
    capacity = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='events')
    sponsor = models.ForeignKey(Sponsor, on_delete=models.SET_NULL, null=True, related_name='sponsored_events')
    date = models.DateTimeField()
    price = models.IntegerField()
    event_planner_name = models.CharField(max_length=255)
    event_planner_contact = models.CharField(max_length=20) # Changed to CharField for leading zeros
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Speaker(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='speakers')
    organisation = models.CharField(max_length=255)
    job_title = models.CharField(max_length=255)
    image = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Attendee(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='attendances')
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='attendees')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name