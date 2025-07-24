@echo off
echo 🚀 Setting up WebChat...
echo.
echo 📋 This will:
echo    • Create fresh database migrations
echo    • Setup SQLite database  
echo    • Create admin user (admin/admin123)
echo.
python setup.py
echo.
echo ✅ Setup complete! 
echo.
echo 📝 Next steps:
echo    1. Start Redis: redis-server (in another terminal)
echo    2. Run server: python manage.py runserver
echo    3. Open: http://127.0.0.1:8000
echo.
echo 🛠️  If you have issues, run:
echo    python reset_db.py
echo.
pause
