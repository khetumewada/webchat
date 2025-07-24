#!/usr/bin/env python
"""
Update database for modern WebChat
"""
import os
import sys
import django
from django.core.management import execute_from_command_line

def update_database():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'webchat.settings')
    django.setup()
    
    print("🔄 Creating migrations...")
    execute_from_command_line(['manage.py', 'makemigrations'])
    
    print("🔄 Applying migrations...")
    execute_from_command_line(['manage.py', 'migrate'])
    
    print("✅ Database updated successfully!")
    print("\n🚀 Your modern WebChat is ready!")
    print("Run: python manage.py runserver")

if __name__ == '__main__':
    update_database()
