#!/bin/bash

echo "🚀 Setting up WebChat Django Application..."

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install requirements
echo "📥 Installing requirements (Django, Channels, Redis)..."
pip install -r requirements.txt

# Make migrations
echo "🗄️ Creating database migrations..."
python manage.py makemigrations

# Apply migrations
echo "🗄️ Applying database migrations..."
python manage.py migrate

# Create superuser (optional)
echo "👤 Creating superuser (optional)..."
echo "You can skip this by pressing Ctrl+C"
python manage.py createsuperuser || echo "Skipped superuser creation"

echo ""
echo "✅ Setup complete!"
echo ""
echo "🚀 To start the application:"
echo "1. Start Redis: redis-server"
echo "2. Start Django: python manage.py runserver"
echo "3. Visit: http://127.0.0.1:8000"
