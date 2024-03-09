from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import UserProfile
from .forms import CustomUserProfileForm


# The profile display function
@login_required(login_url='login-page')
def profile(request):
    user = request.user

    # Working with the display of the user's avatar
    try:
        profile = UserProfile.objects.get(user=user)
    except UserProfile.DoesNotExist:
        profile = None

    return render(request, 'user_profile/profile.html', {'profile': profile})


# # The profile update function
@login_required(login_url='login-page')
def update_profile(request):
    user = request.user

    # Working with the display of the user's avatar
    try:
        profile = UserProfile.objects.get(user=user)
    except UserProfile.DoesNotExist:
        profile = None

    # Changing data
    if request.method == 'POST':
        form = CustomUserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            return redirect('profile')
    else:
        form = CustomUserProfileForm(instance=profile)

    return render(request, 'user_profile/update_profile.html', {'form': form})


# The profile deletion function
@login_required(login_url='login-page')
def delete_profile(request):
    user = request.user

    # Working with the display of the user's avatar
    try:
        profile = UserProfile.objects.get(user=user)
    except UserProfile.DoesNotExist:
        profile = None

    if profile:
        profile.delete()  # Deleting a profile
    user.delete()  # Deleting a user associated with a profile

    return redirect('login-page')