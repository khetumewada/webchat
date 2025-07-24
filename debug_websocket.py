#!/usr/bin/env python
"""
Debug WebSocket setup for WebChat
"""
import os
import sys
import django
from pathlib import Path

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'webchat.settings')
django.setup()

from django.contrib.auth.models import User
from chat.models import Chat, UserProfile

def debug_websocket_setup():
    print("🔍 Debugging WebSocket setup...")
    
    # Check users
    users = User.objects.all()
    print(f"📊 Total users: {users.count()}")
    
    for user in users:
        profile, created = UserProfile.objects.get_or_create(user=user)
        print(f"👤 User: {user.username} (ID: {user.id}) - Profile exists: {not created}")
    
    # Check chats
    chats = Chat.objects.all()
    print(f"💬 Total chats: {chats.count()}")
    
    for chat in chats:
        participants = chat.participants.all()
        print(f"🗨️  Chat {chat.id}: {[p.username for p in participants]}")
        messages_count = chat.messages.count()
        print(f"   Messages: {messages_count}")
    
    # Check Django Channels setup
    try:
        from channels.layers import get_channel_layer
        channel_layer = get_channel_layer()
        print(f"📡 Channel layer: {channel_layer}")
        print(f"📡 Channel layer config: {channel_layer.config if hasattr(channel_layer, 'config') else 'N/A'}")
    except Exception as e:
        print(f"❌ Channel layer error: {e}")
    
    print("\n💡 To test WebSocket:")
    print("1. Make sure Redis is running: redis-server")
    print("2. Start Django: python manage.py runserver")
    print("3. Open browser console and check for WebSocket connection logs")
    print("4. Try sending a message and check console for errors")

if __name__ == '__main__':
    debug_websocket_setup()
