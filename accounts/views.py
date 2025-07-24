from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from django.utils import timezone
from django.contrib import messages
from .models import UserProfile
from .forms import UserProfileForm

def register_view(request):
    if request.user.is_authenticated:
        return redirect('chatapp:home')
        
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Create user profile
            UserProfile.objects.create(user=user)
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, f'Welcome to WebChat, {username}!')
            return redirect('chatapp:home')
    else:
        form = UserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})

@login_required
def logout_view(request):
    # Update user offline status before logout
    try:
        profile = UserProfile.objects.get(user=request.user)
        profile.is_online = False
        profile.last_seen = timezone.now()
        profile.save()
    except UserProfile.DoesNotExist:
        pass
    
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('accounts:welcome')

@login_required
def profile_view(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=profile, user=request.user)
        if form.is_valid():
            # Update user fields
            request.user.first_name = form.cleaned_data['first_name']
            request.user.last_name = form.cleaned_data['last_name']
            request.user.email = form.cleaned_data['email']
            request.user.save()
            
            # Update profile
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('accounts:profile')
    else:
        form = UserProfileForm(instance=profile, user=request.user)
    
    return render(request, 'accounts/profile.html', {'form': form, 'profile': profile})

def welcome_view(request):
    if request.user.is_authenticated:
        return redirect('chatapp:home')
    return render(request, 'accounts/welcome.html')
