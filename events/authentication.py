"""
Authentication backend for Clerk.com
"""
import jwt
import requests
import json
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.conf import settings
from .models import User
from jwt.algorithms import RSAAlgorithm

class ClerkAuthentication(BaseAuthentication):
    """
    Custom authentication class for Django REST Framework to verify Clerk JWTs.
    """
    def authenticate(self, request):
        # Extract the token from the Authorization header
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            # No token provided. Anonymous users are handled by permission classes.
            return None

        token = auth_header.split(' ')[1]

        try:
            # 1. Fetch JWKS from Clerk to verify the token signature
            # Note: In production, you should cache this result to avoid an API call on every request.
            jwks_url = 'https://api.clerk.com/v1/jwks'
            headers = {'Authorization': f'Bearer {settings.CLERK_SECRET_KEY}'}
            jwks_response = requests.get(jwks_url, headers=headers)
            jwks_response.raise_for_status()
            jwks_data = jwks_response.json()

            # 2. Decode the token header to find the Key ID (kid)
            unverified_header = jwt.get_unverified_header(token)
            kid = unverified_header.get('kid')

            # 3. Find the correct public key
            public_key = None
            for key in jwks_data['keys']:
                if key['kid'] == kid:
                    public_key = RSAAlgorithm.from_jwk(json.dumps(key))
                    break
            
            if not public_key:
                raise AuthenticationFailed('Invalid token: Key ID not found.')

            # 4. Verify the token
            payload = jwt.decode(token, public_key, algorithms=['RS256'], options={"verify_aud": False}, leeway=5)
            clerk_user_id = payload.get('sub')

        except Exception as e:
            raise AuthenticationFailed(f'Invalid Clerk token: {str(e)}')

        if not clerk_user_id:
            raise AuthenticationFailed('Clerk user ID not found in token.')

        # Get or create the user in the local database
        try:
            # Try to find the user by their Clerk ID first
            user = User.objects.get(clerk_user_id=clerk_user_id)
        except User.DoesNotExist:
            # If the user doesn't exist, fetch their details from Clerk and create them
            try:
                # Fetch user details from Clerk Backend API
                user_url = f'https://api.clerk.com/v1/users/{clerk_user_id}'
                headers = {'Authorization': f'Bearer {settings.CLERK_SECRET_KEY}'}
                user_response = requests.get(user_url, headers=headers)
                user_response.raise_for_status()
                clerk_user = user_response.json()

                # Extract email
                email_addresses = clerk_user.get('email_addresses', [])
                primary_email_id = clerk_user.get('primary_email_address_id')
                email_address = next((e['email_address'] for e in email_addresses if e['id'] == primary_email_id), None)

                if not email_address:
                    raise AuthenticationFailed("User doesn't have a primary email address in Clerk.")

                # Use update_or_create to link an existing user by email, or create a new one.
                user, created = User.objects.update_or_create(
                    email=email_address,
                    defaults={
                        'clerk_user_id': clerk_user_id,
                        'username': clerk_user.get('username') or email_address.split('@')[0],
                        'first_name': clerk_user.get('first_name', ''),
                        'last_name': clerk_user.get('last_name', ''),
                        'is_active': True,
                        'is_email_verified': True, # Assumed verified by Clerk
                    }
                )
                if created:
                    user.set_unusable_password()
                    user.save()
            except Exception as e:
                raise AuthenticationFailed(f'Could not fetch user details from Clerk or create user: {e}')

        return (user, None) # Authentication successful