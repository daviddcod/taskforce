from django.urls import path
from . import views

app_name = 'myblog'  # This defines the namespace for this URLs module


urlpatterns = [
    path('', views.blog_list, name='blog_list'),
    path('blog/<int:pk>/', views.blog_detail, name='blog_detail'),
    path('blog/new/', views.blog_new, name='blog_new'),
]
