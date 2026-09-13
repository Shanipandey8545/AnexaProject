from django.db import models
from django.contrib.auth.models import AbstractUser
import os


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
    
    

class UploadedAsset(models.Model):
    title = models.CharField(max_length=500)
    file = models.FileField(upload_to='anexa_assets/')
    file_url = models.URLField(max_length=1000, blank=True)
    file_type = models.CharField(max_length=500, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # 1. Pehle actual file se extension nikalein (before or after upload)
        original_ext = ''
        if self.file:
            file_name_str = getattr(self.file, 'name', '') or str(self.file)
            clean_name = file_name_str.split('?')[0].split('#')[0]
            if '.' in clean_name:
                original_ext = clean_name.rsplit('.', 1)[-1].lower()[:10]

        super().save(*args, **kwargs)

        # 2. Cloudinary URL process karein
        if self.file:
            full_url = self.file.url if hasattr(self.file, 'url') else str(self.file)
            if full_url.startswith('http://'):
                full_url = full_url.replace('http://', 'https://', 1)

            # Agar original extension mil gaya ho toh wahi use karein, warna URL se dekhein
            ext = original_ext
            if not ext and '.' in full_url:
                clean_url = full_url.split('?')[0].split('#')[0]
                ext = clean_url.rsplit('.', 1)[-1].lower()[:10]

            if not ext:
                ext = 'file'

            # Image files ke liye Cloudinary automatic optimization lagayein
            if ext in ['jpg', 'jpeg', 'png', 'webp', 'svg', 'gif', 'bmp']:
                if '/upload/' in full_url and '/upload/f_auto,q_auto/' not in full_url:
                    full_url = full_url.replace('/upload/', '/upload/f_auto,q_auto/')

            # Database me exact lowercase extension save karein
            UploadedAsset.objects.filter(id=self.id).update(file_url=full_url, file_type=ext)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']