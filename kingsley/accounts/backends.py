"""
Custom authentication backend to allow login with email OR username
"""
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q

User = get_user_model()


class EmailOrUsernameBackend(ModelBackend):
    """
    Custom authentication backend that allows users to login with either
    their email address or a username field (if it exists).
    
    For admin users, also checks if input matches 'admin' as a shortcut.
    """
    
    def authenticate(self, request, username=None, password=None, **kwargs):
        if username is None or password is None:
            return None
        
        # Normalize input
        username = username.strip().lower()
        
        try:
            # Only allow login with email address
            user = User.objects.get(email__iexact=username)
        except User.DoesNotExist:
            return None
        except User.MultipleObjectsReturned:
            # This shouldn't happen with unique=True on email, but safety first
            user = User.objects.filter(email__iexact=username).first()
        
        # Check password and if user can authenticate
        if user.check_password(password) and self.user_can_authenticate(user):
            return user
        
        return None
    
    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
