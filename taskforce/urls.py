from auth_app import views as auth_app_views; from BlogApp import views as BlogApp_views
from django.conf import settings
from django.conf.urls.static import static

"""
URL configuration for taskforce project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth_app/register/', auth_app_views.register, name='auth_app_register'),
    path('auth_app/user_login/', auth_app_views.user_login, name='auth_app_user_login'),
    path('auth_app/user_logout/', auth_app_views.user_logout, name='auth_app_user_logout'),
    path('auth_app/home/', auth_app_views.home, name='auth_app_home'),
    path('auth_app/dashboard/', auth_app_views.dashboard, name='auth_app_dashboard'),
    path('bloghome/', BlogApp_views.bloghome, name='bloghome'),
    path('bloghome/blog', BlogApp_views.blogindex, name='blogindex'),
    path('music/', include('music.urls')),
    path('blog/', include('BlogApp.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
