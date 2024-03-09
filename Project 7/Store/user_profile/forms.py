from django import forms
from .models import UserProfile


# Creating a profile form
class CustomUserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['first_name', 'last_name', 'email', 'avatar', 'phone_number']