# WebChat - Clean & Modern Django Chat App

A WhatsApp-like real-time chat application with a clean, organized structure.

## 🏗️ Clean Project Structure

\`\`\`
webchat/
├── accounts/              # User Authentication & Profiles
│   ├── models.py         # UserProfile model
│   ├── views.py          # Auth views, profile management
│   ├── forms.py          # Profile forms
│   ├── urls.py           # Auth URLs
│   └── templates/accounts/  # Auth templates (login, register, profile, welcome)
├── chatapp/              # All Chat Features
│   ├── models.py         # Chat, Message models
│   ├── views.py          # Chat views, API endpoints
│   ├── consumers.py      # WebSocket handling
│   ├── templatetags.py   # Template filters
│   ├── routing.py        # WebSocket routing
│   ├── urls.py           # Chat URLs
│   └── templates/chatapp/  # Chat templates (home, room)
├── templates/            # Shared templates (base.html)
├── webchat/             # Django project settings
└── manage.py
\`\`\`

## 🚀 Quick Setup

1. **Setup the project:**
   \`\`\`bash
   python setup.py
   \`\`\`

2. **Start Redis server:**
   \`\`\`bash
   redis-server
   \`\`\`

3. **Run the application:**
   \`\`\`bash
   python manage.py runserver
   \`\`\`

4. **Access the app:**
   - Main app: http://127.0.0.1:8000
   - Admin: http://127.0.0.1:8000/admin

## ✨ Features

- 🔐 **Clean Authentication** - Single set of auth templates
- 💬 **Real-time Chat** - WebSocket-powered instant messaging
- 👥 **User Search** - Find and start conversations
- 📱 **Responsive Design** - Perfect on all devices
- 🎨 **Modern UI** - Clean, properly sized interface
- ⚡ **Fast & Efficient** - Optimized performance

## 🎯 Perfect Structure

- **No duplicate templates** - Single login/register templates
- **Single chat app** - All chat features in one place
- **Proper sizing** - No oversized elements
- **Modern send button** - Beautiful arrow animation
- **Fixed profile page** - Full-page layout
- **Clean code** - Well-organized and maintainable

## 📱 Usage

1. **Register** - Create your account at `/accounts/register/`
2. **Login** - Sign in at `/accounts/login/`
3. **Search Users** - Find people to chat with
4. **Start Chatting** - Real-time messaging
5. **Profile** - Update your information at `/accounts/profile/`

## 🛠️ Technology Stack

- **Backend:** Django 5.0, Django Channels
- **Database:** SQLite (dev), PostgreSQL (prod)
- **Real-time:** WebSockets, Redis
- **Frontend:** Modern HTML5, CSS3, JavaScript
- **Authentication:** Django's built-in auth

## 📝 License

MIT License - Open source and free to use.
