#!/usr/bin/env python
"""
Reset WebChat Database - Clean Start
"""
import os
import sys
import shutil
import django
from django.core.management import execute_from_command_line

def reset_database():
    print("🔄 Resetting WebChat database...")
    
    # Set Django settings
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'webchat.settings')
    
    # Remove database file
    if os.path.exists('db.sqlite3'):
        os.remove('db.sqlite3')
        print("🗑️  Removed old database")
    
    # Remove migration files
    for app in ['accounts', 'chatapp']:
        migrations_dir = f'{app}/migrations'
        if os.path.exists(migrations_dir):
            shutil.rmtree(migrations_dir)
            print(f"🗑️  Removed {app} migrations")
        os.makedirs(migrations_dir, exist_ok=True)
        # Create __init__.py in migrations directory
        with open(f'{migrations_dir}/__init__.py', 'w') as f:
            f.write('')
    
    # Setup Django
    django.setup()
    
    print("📦 Creating fresh migrations...")
    try:
        execute_from_command_line(['manage.py', 'makemigrations', 'accounts'])
        execute_from_command_line(['manage.py', 'makemigrations', 'chatapp'])
    except Exception as e:
        print(f"❌ Migration creation failed: {e}")
        return
    
    print("🔄 Applying migrations...")
    try:
        execute_from_command_line(['manage.py', 'migrate'])
    except Exception as e:
        print(f"❌ Migration application failed: {e}")
        return
    
    print("👤 Creating superuser...")
    try:
        from django.contrib.auth.models import User
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
            print("✅ Superuser created: admin/admin123")
        else:
            print("ℹ️  Superuser already exists")
    except Exception as e:
        print(f"⚠️  Superuser creation failed: {e}")
    
    print("✅ Database reset complete!")
    print("\n🚀 Next Steps:")
    print("   1. Start Redis: redis-server")
    print("   2. Run server: python manage.py runserver")
    print("   3. Open: http://127.0.0.1:8000")

if __name__ == '__main__':
    reset_database()
