from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    """Extended user profile for livestock management"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    
    # Contact information
    phone_number = models.CharField(max_length=20, blank=True)
    organization = models.CharField(max_length=255, blank=True)
    
    # Preferences
    timezone = models.CharField(max_length=100, default='UTC')
    language = models.CharField(
        max_length=10,
        choices=[
            ('en', 'English'),
            ('es', 'Spanish'),
            ('fr', 'French'),
            ('de', 'German'),
        ],
        default='en'
    )
    
    # Verification
    email_verified = models.BooleanField(default=False)
    phone_verified = models.BooleanField(default=False)
    
    # Account status
    is_active = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.username}'s Profile"
    
    class Meta:
        verbose_name_plural = 'User Profiles'
