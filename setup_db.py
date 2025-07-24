#!/usr/bin/env python
"""
Simple database setup script for WebChat
"""
import os
import sys
import django
from django.core.management import execute_from_command_line

def setup_database():
    """Setup the database with migrations"""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'webchat.settings')
    django.setup()
    
    print("🗄️  Creating database migrations...")
    execute_from_command_line(['manage.py', 'makemigrations'])
    
    print("🗄️  Applying database migrations...")
    execute_from_command_line(['manage.py', 'migrate'])
    
    print("✅ Database setup complete!")
    print("\n🚀 Next steps:")
    print("1. Start Redis: redis-server")
    print("2. Run Django: python manage.py runserver")
    print("3. Visit: http://127.0.0.1:8000/register/")

if __name__ == '__main__':
    setup_database()
