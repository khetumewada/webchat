#!/usr/bin/env python
"""
Check WebChat setup and fix common issues
"""
import os
import sys
import django
from pathlib import Path

def check_setup():
    print("🔍 Checking WebChat setup...")
    
    # Check if we're in the right directory
    if not Path('manage.py').exists():
        print("❌ manage.py not found. Make sure you're in the project root directory.")
        return False
    
    # Check if migrations directory exists
    migrations_dir = Path('chat/migrations')
    if not migrations_dir.exists():
        print("📁 Creating migrations directory...")
        migrations_dir.mkdir(parents=True, exist_ok=True)
        
        # Create __init__.py
        init_file = migrations_dir / '__init__.py'
        init_file.write_text('')
        print("✅ Created migrations directory")
    
    # Check for migration files
    migration_files = list(migrations_dir.glob('*.py'))
    migration_files = [f for f in migration_files if f.name != '__init__.py']
    
    if not migration_files:
        print("⚠️  No migration files found. Need to create migrations.")
        return False
    else:
        print(f"✅ Found {len(migration_files)} migration files")
    
    # Check database
    db_file = Path('db.sqlite3')
    if not db_file.exists():
        print("⚠️  Database file doesn't exist. Need to run migrations.")
        return False
    else:
        print("✅ Database file exists")
    
    return True

def run_setup():
    print("\n🔧 Running setup commands...")
    
    # Set Django settings
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'webchat.settings')
    
    try:
        # Import Django and setup
        django.setup()
        from django.core.management import execute_from_command_line
        
        print("📝 Creating migrations...")
        execute_from_command_line(['manage.py', 'makemigrations'])
        
        print("🗄️  Applying migrations...")
        execute_from_command_line(['manage.py', 'migrate'])
        
        print("✅ Setup complete!")
        return True
        
    except Exception as e:
        print(f"❌ Error during setup: {e}")
        return False

if __name__ == '__main__':
    if not check_setup():
        print("\n🔧 Issues found. Running setup...")
        if run_setup():
            print("\n🎉 Setup successful! You can now run:")
            print("   python manage.py runserver")
        else:
            print("\n❌ Setup failed. Please check the errors above.")
    else:
        print("\n✅ Setup looks good! You can run:")
        print("   python manage.py runserver")
