from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.chat_home, name='chat_home'),
    path('register/', views.register_view, name='register'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('chat/<int:chat_id>/', views.chat_room, name='chat_room'),
    path('start-chat/<int:user_id>/', views.start_chat, name='start_chat'),
    path('api/chat/<int:chat_id>/messages/', views.get_chat_messages, name='get_chat_messages'),
    path('api/search-users/', views.search_users, name='search_users'),
]
