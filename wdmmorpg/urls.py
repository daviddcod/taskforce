from django.urls import path
from . import views

app_name = 'wdm'

urlpatterns = [
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('register/', views.register_user, name='register_user'),
    path('profile/update/', views.update_profile, name='update_profile'),
    path('user/stats/', views.user_stats_view, name='user-stats'),
    path('tasklist', views.task_list, name='task_list'),
    path('task/<int:pk>/', views.task_detail, name='task_detail'),
    path('task/new/', views.task_create, name='task_create'),
    path('task/<int:pk>/edit/', views.task_update, name='task_update'),
    path('task/<int:pk>/delete/', views.task_delete, name='task_delete'),
    path('environment/add/', views.add_environment, name='add_environment'),
    path('environment/list/', views.environment_list, name='envlist'),
    path('environment/update/<int:pk>/', views.update_environment, name='update_environment'),
    path('environment/delete/<int:pk>/', views.delete_environment, name='delete_environment'),
    path('rank/create/', views.create_rank, name='create_rank'),
    path('rank/', views.list_rank, name='rank_list'),
    path('rank/update/<int:pk>/', views.update_rank, name='update_rank'),
    path('rank/delete/<int:pk>/', views.delete_rank, name='delete_rank'),
    path('priorityscale/add/', views.create_priorityscale, name='create_priorityscale'),    path('priorityscale/', views.list_priorityscale, name='priorityscale_list'),
    path('priorityscale/update/<int:pk>/', views.update_priorityscale, name='update_priorityscale'),
    path('priorityscale/delete/<int:pk>/', views.delete_priorityscale, name='delete_priorityscale'),
    path('profile/create/', views.profile_create, name='profile_create'),
    path('profile/success/', views.profile_success, name='profile_success'),
    #Missions#
    path('missions/', views.mission_list, name='mission_list'),
    path('missions/create/', views.create_mission, name='create_mission'),
    path('missions/<int:pk>/', views.mission_detail, name='mission_detail'),
    path('missions/<int:pk>/edit/', views.update_mission, name='update_mission'),
    path('missions/<int:pk>/delete/', views.delete_mission, name='delete_mission'),
    #projects#
    path('projects/', views.project_list, name='project_list'),
    path('project/create/', views.create_project, name='create_project'),
    path('project/<int:pk>/', views.project_detail, name='project_detail'),
    path('project/<int:pk>/update/', views.update_project, name='update_project'),
    path('project/<int:pk>/delete/', views.delete_project, name='delete_project'),
    # Add other paths as needed
    path('complete_task/<int:task_id>/', views.complete_task, name='complete_task'),
    path('completed_tasks/', views.completed_tasks, name='completed_tasks'),
    path('project/update/<int:project_id>/', views.update_project, name='update_project'),

    path('profile/', views.user_profile, name='user_profile'),

    path('objectives/', views.objective_overview, name='objective_overview'),

    path('objectives/project/<int:project_id>/', views.objective_overview, name='objective_overview_project'),
]

