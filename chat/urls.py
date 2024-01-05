# chat/urls.py

from django.urls import path
from . import views

app_name = 'chat'  # This defines the namespace for this URLs module


urlpatterns = [
    path('', views.index, name='index'),  # The index view where users select a chat room
    path('<str:room_name>/', views.room, name='room'),  # The view for an individual chat room
]
