

from django.urls import path
from . import views

app_name = 'auth_app'  # This defines the namespace for this URLs module


urlpatterns = [
    path('register/', views.register, name='user_register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('home/', views.home, name='user_home'),
    path('dashboard/', views.dashboard, name='user_dashboard'),
]
