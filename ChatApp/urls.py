from django.urls import path
from . import views

app_name = 'chatapp'
urlpatterns = [
    path('home/', views.chat_home, name='home'),
    path('chat/<int:chat_id>/', views.chat_room, name='room'),
    path('start-chat/<int:user_id>/', views.start_chat, name='start_chat'),
    path('api/chat/<int:chat_id>/messages/', views.get_chat_messages, name='get_chat_messages'),
    path('api/search-users/', views.search_users, name='search_users'),
]
