from django import forms
from django.db import models
from mainpage.models import CustomUser


# The user profile model
class UserProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='profile')
    username = models.CharField(max_length=150, unique=True)
    first_name = models.CharField(max_length=50, default="-")
    last_name = models.CharField(max_length=50, default="-")
    email = models.EmailField()
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True, default='avatars/default.png')
    phone_number = models.CharField(max_length=20, null=True, blank=True, default="-")

    def save(self, *args, **kwargs):
        self.username = self.user.username
        self.email = self.user.email
        super(UserProfile, self).save(*args, **kwargs)

    def __str__(self):
        return self.user.username