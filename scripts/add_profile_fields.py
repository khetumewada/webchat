#!/usr/bin/env python
"""
Add new profile fields migration
"""
import os
import sys
import django
from django.core.management import execute_from_command_line

def create_migration():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'webchat.settings')
    django.setup()
    
    print("🔄 Creating migration for new profile fields...")
    execute_from_command_line(['manage.py', 'makemigrations'])
    
    print("🔄 Applying migrations...")
    execute_from_command_line(['manage.py', 'migrate'])
    
    print("✅ Profile fields migration completed!")

if __name__ == '__main__':
    create_migration()
