from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.



class User(AbstractUser):
    ROLE_TYPE = [
        ('SuperAdmin','SuperAdmin'),
        ('Admin','Admin'),
        ('Customer','Customer'),
    ]
    
    role = models.CharField(max_length=50, choices=ROLE_TYPE, default='Admin')
    phone = models.CharField(max_length=15,null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    profile_image = models.FileField(upload_to='user_profile', null=True, blank=True)
    license_number = models.CharField(max_length=100, null=True, blank=True)
    aadhar_number = models.CharField(max_length=20, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    