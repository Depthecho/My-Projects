from django import forms
from .models import UserSettings


class AppearanceSettingsForm(forms.ModelForm):
    class Meta:
        model = UserSettings
        fields = ['appearance_settings']


class ConfidentialitySettingsForm(forms.ModelForm):
    class Meta:
        model = UserSettings
        fields = ['confidentiality_settings']


class ChangePasswordForm(forms.Form):
    current_password = forms.CharField(label='Current Password', widget=forms.PasswordInput)
    new_password1 = forms.CharField(label='New Password', widget=forms.PasswordInput)
    new_password2 = forms.CharField(label='Confirm New Password', widget=forms.PasswordInput)