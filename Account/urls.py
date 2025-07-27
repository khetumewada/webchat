from django.urls import path
from django.contrib.auth import views as auth_views
from . import views


app_name = 'account'
urlpatterns = [
    path('welcome/', views.welcome_view, name='welcome'),
    path('profile/', views.profile_view, name='profile'),
    path('register/', views.register_view, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='account/login.html'), name='login'),
    path('logout/', views.logout_view, name='logout'),
]