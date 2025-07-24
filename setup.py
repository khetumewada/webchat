#!/usr/bin/env python
"""
Setup WebChat - Simple and Clean
"""
import os
import sys
import django
from django.core.management import execute_from_command_line

def setup_webchat():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'webchat.settings')
    django.setup()
    
    print("🔄 Setting up WebChat...")
    
    print("📦 Creating migrations...")
    execute_from_command_line(['manage.py', 'makemigrations', 'accounts'])
    execute_from_command_line(['manage.py', 'makemigrations', 'chatapp'])
    
    print("🔄 Applying migrations...")
    execute_from_command_line(['manage.py', 'migrate'])
    
    print("✅ WebChat setup complete!")
    print("\n🎯 **Clean Structure:**")
    print("   • accounts/ - Authentication & User Management")
    print("   • chatapp/ - All Chat Features")
    print("   • No unnecessary folders or files")
    print("   • Perfect sizing and modern UI")
    print("\n🚀 Run: python manage.py runserver")

if __name__ == '__main__':
    setup_webchat()
