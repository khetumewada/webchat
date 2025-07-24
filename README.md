# WebChat - Django Real-time Chat Application

A WhatsApp-like real-time chat application built with Django, Django Channels, and WebSockets.

## Features

- 🔐 User authentication (register, login, logout)
- 💬 Real-time messaging with WebSockets
- 👥 Private conversations
- ⌨️ Typing indicators
- 🟢 Online/offline status
- 📱 Responsive design (mobile-friendly)
- 🔍 User search functionality

## Prerequisites

- Python 3.8+
- Redis server
- pip (Python package manager)

## Quick Setup

### Option 1: Using Setup Scripts (Recommended)

**For Linux/macOS:**
\`\`\`bash
chmod +x setup.sh
./setup.sh
\`\`\`

**For Windows:**
\`\`\`cmd
setup.bat
\`\`\`

### Option 2: Manual Setup

1. **Create virtual environment:**
\`\`\`bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
\`\`\`

2. **Install dependencies:**
\`\`\`bash
pip install -r requirements.txt
\`\`\`

3. **Setup database:**
\`\`\`bash
python manage.py makemigrations
python manage.py migrate
\`\`\`

4. **Create superuser (optional):**
\`\`\`bash
python manage.py createsuperuser
\`\`\`

## Running the Application

1. **Start Redis server:**
\`\`\`bash
redis-server
\`\`\`

2. **Start Django development server:**
\`\`\`bash
python manage.py runserver
\`\`\`

3. **Access the application:**
- Main app: http://127.0.0.1:8000
- Admin panel: http://127.0.0.1:8000/admin (if you created a superuser)

## Usage

1. **Register Account:** Visit `/register/` to create a new account
2. **Login:** Use your credentials to login
3. **Start Chatting:** 
   - Click the chat button (💬) to search for users
   - Select a user to start a conversation
   - Send messages in real-time!

## Project Structure

\`\`\`
webchat/
├── webchat/                # Django project settings
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py            # ASGI config for WebSockets
│   └── wsgi.py
├── chat/                  # Main chat application
│   ├── models.py          # Database models
│   ├── views.py           # View functions
│   ├── consumers.py       # WebSocket consumers
│   ├── routing.py         # WebSocket routing
│   ├── urls.py           # URL patterns
│   └── admin.py          # Admin configuration
├── templates/             # HTML templates
├── requirements.txt      # Python dependencies
└── manage.py            # Django management script
\`\`\`

## Standard Django Commands

\`\`\`bash
# Database operations
python manage.py makemigrations
python manage.py migrate

# User management
python manage.py createsuperuser

# Development
python manage.py runserver
python manage.py shell
python manage.py collectstatic
\`\`\`

## Technology Stack

- **Backend:** Django 4.2, Django Channels
- **Database:** SQLite (development), PostgreSQL (production)
- **Real-time:** WebSockets, Redis
- **Frontend:** HTML5, CSS3, JavaScript (Vanilla)
- **Authentication:** Django's built-in auth system

## Development

### Testing Multiple Users

Open the application in multiple browser windows/tabs or different browsers to simulate multiple users chatting.

## Troubleshooting

**Redis Connection Error:**
- Make sure Redis server is running: `redis-server`
- Check Redis connection: `redis-cli ping`

**WebSocket Connection Failed:**
- Ensure Django Channels is properly configured
- Check browser console for WebSocket errors
- Verify ASGI application is running

**Database Issues:**
- Delete `db.sqlite3` and run migrations again
- Check for migration conflicts

## License

This project is open source and available under the MIT License.
