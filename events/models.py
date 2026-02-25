from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
import random
import datetime

class User(AbstractUser):
    email = models.EmailField(unique=True)
    password_digest = models.CharField(max_length=100, null=True, blank=True)
    age = models.IntegerField(null=True, blank=True)
    gender = models.CharField(max_length=20, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    admin = models.BooleanField(default=False)
    is_email_verified = models.BooleanField(default=False)
    recovery_pin = models.CharField(max_length=10, null=True, blank=True)
    otp_code = models.CharField(max_length=6, null=True, blank=True)
    otp_created_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.username

    def generate_otp(self):
        self.otp_code = f"{random.randint(100000, 999999)}"
        self.otp_created_at = timezone.now()
        self.save()
        return self.otp_code

    def verify_otp(self, entered_otp):
        if not self.otp_code or not self.otp_created_at: return False
        if self.otp_code != entered_otp: return False
        if timezone.now() > self.otp_created_at + datetime.timedelta(minutes=10): return False
        return True


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