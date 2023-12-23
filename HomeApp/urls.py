from django.urls import path
from . import views;

app_name = 'home_app'  # This defines the namespace for this URLs module


urlpatterns = [
    path('', views.home, name='home'),
    path('set_cookie', views.set_cookie, name='set_cookie'),

]