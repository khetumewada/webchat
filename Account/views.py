from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone

from .models import UserProfile
from .forms import UserProfileForm, CustomRegisterForm


def register_view(request):
    """Handle user registration with profile creation."""
    if request.user.is_authenticated:
        return redirect('chatapp:home')

    if request.method == 'POST':
        form = CustomRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            UserProfile.objects.create(user=user)
            login(request, user)
            messages.success(request, f'Welcome to WebChat, {user.username}!')
            return redirect('chatapp:home')
        # If invalid, will fall through and render with errors
    else:
        form = CustomRegisterForm()

    return render(request, 'account/register.html', {'form': form})


@login_required
def logout_view(request):
    """
    Log user out and update online status.
    """
    try:
        profile = UserProfile.objects.get(user=request.user)
        profile.is_online = False
        profile.last_seen = timezone.now()
        profile.save()

    except UserProfile.DoesNotExist:
        pass  # Not critical

    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('account:welcome')


@login_required
def profile_view(request):
    """
    View and update user profile and base user details (first name, last name, email).
    """
    profile, create = UserProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        form.fields['first_name'].initial = request.user.first_name
        form.fields['last_name'].initial = request.user.last_name
        form.fields['email'].initial = request.user.email

        if form.is_valid():
            # Update the User fields
            request.user.first_name = form.cleaned_data.get('first_name', request.user.first_name)
            request.user.last_name = form.cleaned_data.get('last_name', request.user.last_name)
            request.user.email = form.cleaned_data.get('email', request.user.email)
            request.user.save()

            # Save UserProfile fields
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('account:profile')
    else:
        form = UserProfileForm(instance=profile)
        # Prepopulate User fields
        form.fields['first_name'].initial = request.user.first_name
        form.fields['last_name'].initial = request.user.last_name
        form.fields['email'].initial = request.user.email

    return render(request, 'account/profile.html', {'form': form, 'profile': profile})


def welcome_view(request):
    """Show welcome page to unauthenticated users."""
    if request.user.is_authenticated:
        return redirect('chatapp:home')
    return render(request, 'account/welcome.html')