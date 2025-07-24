#!/usr/bin/env python
"""
Quick Fix for WebChat Issues
"""
import os
import sys
import shutil

def quick_fix():
    print("🔧 Quick Fix for WebChat...")
    
    # Create templatetags directory structure
    templatetags_dir = 'chatapp/templatetags'
    if not os.path.exists(templatetags_dir):
        os.makedirs(templatetags_dir, exist_ok=True)
        print(f"📁 Created {templatetags_dir} directory")
    
    # Create __init__.py if it doesn't exist
    init_file = f'{templatetags_dir}/__init__.py'
    if not os.path.exists(init_file):
        with open(init_file, 'w') as f:
            f.write('# Empty file to make templatetags a Python package\n')
        print(f"📄 Created {init_file}")
    
    print("✅ Template tags structure fixed!")
    print("\n🚀 Now run:")
    print("   python reset_db.py")
    print("   python manage.py runserver")

if __name__ == '__main__':
    quick_fix()
