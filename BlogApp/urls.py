"""
URL configuration for WDMMORPG2 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from BlogApp import views as blog_views; #Line 24 is sensitive for scaffolding reasons, make sure that nothing else but path references inhabit that line

urlpatterns = [
    path('bloglist', blog_views.blog_list, name='blog-list'),
    path('<int:pk>/', blog_views.blog_detail, name='blog-detail'),
    path('create/', blog_views.blog_create, name='blog-create'),
    path('<int:pk>/edit/', blog_views.blog_edit, name='blog-edit'),
    path('<int:pk>/delete/', blog_views.blog_delete, name='blog-delete'),
]
