# plan_selection/urls.py

from django.urls import path
from .views import select_plan, list_plans

app_name = 'plan_selection'  # This defines the namespace for this URLs module

urlpatterns = [
    path('select/', select_plan, name='select_plan'),
    path('plans/', list_plans, name='list_plans'),
    path('list/', list_plans, name='list_plans'),  # Maps to the list_plans view

]
