from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('register/', views.register_user, name='register_user'),
    path('profile/update/', views.update_profile, name='update_profile'),
    path('user/stats/', views.user_stats_view, name='user-stats'),

]

