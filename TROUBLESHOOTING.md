# WebChat Troubleshooting Guide

## Common Issues & Solutions

### 1. Database Error: "no such table: accounts_userprofile"

**Problem:** Database tables haven't been created.

**Solution:**
\`\`\`bash
python reset_db.py
python manage.py runserver
\`\`\`

### 2. WebSocket Connection Failed

**Problem:** Redis server is not running.

**Solution:**
\`\`\`bash
# Start Redis server (in a separate terminal)
redis-server

# Then start Django
python manage.py runserver
\`\`\`

### 3. Migration Issues

**Problem:** Migration conflicts or errors.

**Solution:**
\`\`\`bash
# Reset everything
python reset_db.py

# Or manually:
rm db.sqlite3
rm -rf accounts/migrations
rm -rf chatapp/migrations
python setup.py
\`\`\`

### 4. Port Already in Use

**Problem:** Port 8000 is already in use.

**Solution:**
\`\`\`bash
# Use a different port
python manage.py runserver 8001
\`\`\`

### 5. Permission Errors (Linux/Mac)

**Problem:** Permission denied errors.

**Solution:**
\`\`\`bash
chmod +x setup.sh
chmod +x reset_db.py
./setup.sh
\`\`\`

## Fresh Install Steps

1. **Complete Reset:**
   \`\`\`bash
   python reset_db.py
   \`\`\`

2. **Start Redis:**
   \`\`\`bash
   redis-server
   \`\`\`

3. **Run Server:**
   \`\`\`bash
   python manage.py runserver
   \`\`\`

4. **Access App:**
   - Main: http://127.0.0.1:8000
   - Admin: http://127.0.0.1:8000/admin (admin/admin123)

## Getting Help

- Check the error message carefully
- Ensure Redis is running
- Try a fresh database reset
- Make sure all dependencies are installed: `pip install -r requirements.txt`
