#!/usr/bin/env python
"""
Setup script for WebChat Django application
This script installs dependencies and sets up the database
"""
import os
import sys
import subprocess

def run_command(command, description):
    """Run a system command and handle errors"""
    print(f"✅ {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"   ✓ {description} completed successfully")
        return result
    except subprocess.CalledProcessError as e:
        print(f"   ❌ Error in {description}: {e}")
        print(f"   Output: {e.stdout}")
        print(f"   Error: {e.stderr}")
        return None

def main():
    """Main setup function"""
    print("🚀 Setting up WebChat Django Application")
    print("=" * 50)
    
    # Install dependencies
    print("\n📦 Installing Python dependencies...")
    pip_commands = [
        "python3 -m pip install --user Django==5.0.1",
        "python3 -m pip install --user channels==4.0.0", 
        "python3 -m pip install --user channels-redis==4.2.0",
        "python3 -m pip install --user redis==5.0.1",
        "python3 -m pip install --user asgiref==3.7.2"
    ]
    
    for cmd in pip_commands:
        result = run_command(cmd, f"Installing {cmd.split()[-1]}")
        if result is None:
            print("❌ Failed to install dependencies")
            return False
    
    # Run migrations
    print("\n🗄️ Setting up database...")
    if run_command("python3 manage.py makemigrations", "Creating migrations"):
        run_command("python3 manage.py migrate", "Applying migrations")
    else:
        print("❌ Failed to create migrations")
        return False
    
    # Create superuser (optional)
    print("\n👤 Creating superuser (optional)...")
    print("   💡 You can create a superuser later with: python3 manage.py createsuperuser")
    
    # Success message
    print("\n🎉 Setup completed successfully!")
    print("=" * 50)
    print("📋 Next steps:")
    print("   1. Start Redis server: redis-server")
    print("   2. Run the app: python3 manage.py runserver")
    print("   3. Visit: http://127.0.0.1:8000")
    print("   4. Admin panel: http://127.0.0.1:8000/admin")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
