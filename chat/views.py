from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.db.models import Q, Max
from django.utils import timezone
from django.contrib import messages
from .models import Chat, Message, UserProfile, MessageRead
from .forms import UserProfileForm
import json

def root_view(request):
    """Handle root URL - redirect based on authentication status"""
    if request.user.is_authenticated:
        return redirect('chat_home')
    return redirect('welcome')

def register_view(request):
    if request.user.is_authenticated:
        return redirect('chat_home')
        
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
            return redirect('chat_home')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

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
    return redirect('welcome')

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
            return redirect('profile')
    else:
        form = UserProfileForm(instance=profile, user=request.user)
    
    return render(request, 'chat/profile.html', {'form': form, 'profile': profile})

@login_required
def chat_home(request):
    # Update user online status
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    profile.is_online = True
    profile.last_seen = timezone.now()
    profile.save()
    
    # Get user's chats
    user_chats = Chat.objects.filter(participants=request.user).annotate(
        last_message_time=Max('messages__timestamp')
    ).order_by('-last_message_time')
    
    context = {
        'chats': user_chats,
        'current_user': request.user,
    }
    return render(request, 'chat/home.html', context)

@login_required
def chat_room(request, chat_id):
    chat = get_object_or_404(Chat, id=chat_id, participants=request.user)
    messages_list = chat.messages.all().order_by('timestamp')
    
    # Mark messages as read
    unread_messages = messages_list.exclude(sender=request.user).exclude(
        read_by__user=request.user
    )
    for message in unread_messages:
        MessageRead.objects.get_or_create(message=message, user=request.user)
    
    # Get user's chats for sidebar
    user_chats = Chat.objects.filter(participants=request.user).annotate(
        last_message_time=Max('messages__timestamp')
    ).order_by('-last_message_time')
    
    context = {
        'chat': chat,
        'messages': messages_list,
        'current_user': request.user,
        'chats': user_chats,
        'active_chat_id': chat_id,
    }
    return render(request, 'chat/room.html', context)

@login_required
def start_chat(request, user_id):
    other_user = get_object_or_404(User, id=user_id)
    
    # Prevent users from starting chat with themselves
    if other_user == request.user:
        messages.error(request, "You cannot start a chat with yourself.")
        return redirect('chat_home')
    
    # Check if chat already exists
    existing_chat = Chat.objects.filter(
        chat_type='private',
        participants=request.user
    ).filter(participants=other_user).first()
    
    if existing_chat:
        return redirect('chat_room', chat_id=existing_chat.id)
    
    # Create new chat
    chat = Chat.objects.create(chat_type='private')
    chat.participants.add(request.user, other_user)
    
    messages.success(request, f'Started new conversation with {other_user.get_full_name() or other_user.username}')
    return redirect('chat_room', chat_id=chat.id)

@login_required
def get_chat_messages(request, chat_id):
    chat = get_object_or_404(Chat, id=chat_id, participants=request.user)
    messages_list = chat.messages.all().order_by('timestamp')
    
    messages_data = []
    for message in messages_list:
        messages_data.append({
            'id': message.id,
            'sender': message.sender.username,
            'content': message.content,
            'timestamp': message.timestamp.strftime('%I:%M %p'),
            'is_own': message.sender == request.user,
        })
    
    return JsonResponse({'messages': messages_data})

@login_required
def search_users(request):
    query = request.GET.get('q', '')
    if query:
        users = User.objects.filter(
            Q(username__icontains=query) | 
            Q(first_name__icontains=query) | 
            Q(last_name__icontains=query)
        ).exclude(id=request.user.id)[:10]
        
        users_data = []
        for user in users:
            profile = getattr(user, 'userprofile', None)
            users_data.append({
                'id': user.id,
                'username': user.username,
                'full_name': user.get_full_name() or user.username,
                'initials': profile.get_avatar_initials() if profile else user.username[:2].upper(),
                'is_online': profile.is_online if profile else False,
            })
        
        return JsonResponse({'users': users_data})
    
    return JsonResponse({'users': []})

def welcome_view(request):
    if request.user.is_authenticated:
        return redirect('chat_home')
    return render(request, 'chat/welcome.html')
