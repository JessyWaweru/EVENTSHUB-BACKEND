from rest_framework import serializers
from .models import User, Sponsor, Event, Speaker, Attendee


# ===========================
# AUTH SERIALIZERS
# ===========================

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'age']

    def create(self, validated_data):
        # Use create_user to handle password hashing automatically
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            age=validated_data.get('age')
        )
        return user

class LoginRequestSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

class OTPVerifySerializer(serializers.Serializer):
    username = serializers.CharField()
    otp = serializers.CharField(max_length=6)

class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()

class PasswordResetConfirmSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField(max_length=6)
    new_password = serializers.CharField(write_only=True)

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