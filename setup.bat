@echo off
echo 🚀 Setting up WebChat Django Application...

REM Check if virtual environment exists
if not exist "venv" (
    echo 📦 Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo 🔧 Activating virtual environment...
call venv\Scripts\activate

REM Install requirements
echo 📥 Installing requirements (Django, Channels, Redis)...
pip install -r requirements.txt

REM Make migrations
echo 🗄️ Creating database migrations...
python manage.py makemigrations

REM Apply migrations
echo 🗄️ Applying database migrations...
python manage.py migrate

REM Create superuser (optional)
echo 👤 Creating superuser (optional)...
echo You can skip this by pressing Ctrl+C
python manage.py createsuperuser

echo.
echo ✅ Setup complete!
echo.
echo 🚀 To start the application:
echo 1. Start Redis: redis-server
echo 2. Start Django: python manage.py runserver
echo 3. Visit: http://127.0.0.1:8000
pause
