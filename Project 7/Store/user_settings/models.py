from django.db import models
from mainpage.models import CustomUser


class UserSettings(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    appearance_settings = models.CharField(max_length=255, blank=True, null=True)
    confidentiality_settings = models.CharField(max_length=255, blank=True, null=True)


class Setting(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class UserProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    setting = models.ForeignKey(Setting, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.user.username