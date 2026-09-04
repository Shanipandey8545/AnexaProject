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
    
    
    
class ContactForm(models.Model):
    STATUS_CHOICES = [
        ('New', 'New'),
        ('InProgress', 'InProgress'),
        ('Contacted', 'Contacted'),
        ('Converted', 'Converted'),
        ('Closed', 'Closed'),
    ]

    name = models.CharField(max_length=500, null=True, blank=True)
    phone = models.CharField(max_length=500, null=True, blank=True)
    email = models.CharField(max_length=500, null=True, blank=True)
    required_facade_scope = models.CharField(max_length=500, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=50,choices=STATUS_CHOICES,default='new',blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name or 'No Name'}"
    