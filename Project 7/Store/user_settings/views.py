from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import UserProfile
from .forms import AppearanceSettingsForm, ConfidentialitySettingsForm, ChangePasswordForm


# The function of displaying the settings page
def settings_view(request):
    selected_setting = request.GET.get('setting')
    filtered_profiles = UserProfile.objects.all()
    profile = None
    user = request.user

    # Working with the display of the user's avatar
    if user.is_authenticated:
        try:
            profile = UserProfile.objects.get(user=user)
        except UserProfile.DoesNotExist:
            profile = None

    # Working with password change
    if request.method == 'POST':
        password_change_form = ChangePasswordForm(request.POST)
        if password_change_form.is_valid():
            current_password = password_change_form.cleaned_data['current_password']
            new_password1 = password_change_form.cleaned_data['new_password1']
            new_password2 = password_change_form.cleaned_data['new_password2']

            if not request.user.check_password(current_password):
                messages.error(request, 'Invalid current password.')
            else:
                if new_password1 == new_password2:
                    request.user.set_password(new_password1)
                    request.user.save()
                    update_session_auth_hash(request, request.user)
                    messages.success(request, 'Your password was successfully changed.')
                    return redirect('settings')
                else:
                    messages.error(request, 'New passwords do not match.')
    else:
        password_change_form = ChangePasswordForm()

    if selected_setting:
        filtered_profiles = filtered_profiles.filter(setting__name=selected_setting)

    return render(request, 'user_settings/settings.html', {
        'profiles': filtered_profiles,
        'selected_setting': selected_setting,
        'password_change_form': password_change_form,
        'profile': profile,
    })


# The appearance settings display function
def appearance_settings_view(request):
    profile = None
    user = request.user

    # Working with the display of the user's avatar
    if user.is_authenticated:
        try:
            profile = UserProfile.objects.get(user=user)
        except UserProfile.DoesNotExist:
            profile = None

    if request.method == 'POST':
        appearance_settings_form = AppearanceSettingsForm(request.POST)
        if appearance_settings_form.is_valid():
            pass
    else:
        appearance_settings_form = AppearanceSettingsForm()

    return render(request, 'appearance_settings.html', {'appearance_settings_form': appearance_settings_form, 'profile': profile})


# The confidentiality settings display function
@login_required(login_url='login-page')
def confidentiality_settings_view(request):
    profile = None
    user = request.user

    # Working with the display of the user's avatar
    if user.is_authenticated:
        try:
            profile = UserProfile.objects.get(user=user)
        except UserProfile.DoesNotExist:
            pass

    if request.method == 'POST':
        confidentiality_settings_form = ConfidentialitySettingsForm(request.POST)
        if confidentiality_settings_form.is_valid():
            profile = None
    else:
        confidentiality_settings_form = ConfidentialitySettingsForm()

    return render(request, 'confidentiality_settings.html', {'confidentiality_settings_form': confidentiality_settings_form, 'profile': profile})