from auth_app import views as auth_app_views
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
from HomeApp import views as home_views

urlpatterns = [
    path('', include('HomeApp.urls')),
    path('admin/', admin.site.urls),
    path('auth/', include('auth_app.urls')),
    path('music/', include('music.urls')),
    path('blog/', include('myblog.urls')),
    path('wdm/', include(('wdmmorpg.urls', 'wdmmorpg'), namespace='wdm')),
    path('plan-selection/', include(('plan_selection.urls', 'plan-selection'), namespace='plan-selection')),
    path('payment_processor/', include('payment_processor.urls', namespace='payment_processor')),
    path('wdmmorpg/', include('wdmmorpg.urls', namespace='wdmmorpg')),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

