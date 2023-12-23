from django.shortcuts import render, redirect
from .models import UserProfile, Task, Mission, Project, Inventory, Tool, TransportationKey, Consumable, Environment
from .forms import TaskForm, MissionForm, ProjectForm, InventoryForm, UserProfileForm, UserProfile, UserTaskInteraction, UserTaskInteractionForm, CustomUserCreationForm
from django.contrib.auth.decorators import login_required

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import UserProfile, Task, Mission, Project, Inventory, Plan  # Import the Plan model
from .forms import TaskForm, MissionForm, ProjectForm, InventoryForm

@login_required
def dashboard_view(request):
    # Fetch the user profile
    user_profile = UserProfile.objects.get(user=request.user)

    # Check if the user has a plan, if not, assign the default 'Traverser' plan
    if not user_profile.plan:  # Assuming 'plan' field in UserProfile model
        traverser_plan, _ = Plan.objects.get_or_create(
            name='Traverser',
            defaults={  # Default values for creating the 'Traverser' plan
                'description': 'Default plan for new users.',
                'price': 0.00,
                'billing_cycle': 'daily',  # or any other default value
            }
        )
        user_profile.plan = traverser_plan
        user_profile.save()

    # Fetch tasks, missions, projects, and inventory items related to the user
    tasks = Task.objects.filter(environment__user=user_profile)
    missions = Mission.objects.filter(tasks__environment__user=user_profile)
    projects = Project.objects.filter(missions__tasks__environment__user=user_profile)
    inventory = Inventory.objects.get(user=user_profile)

    # Prepare forms (if needed for the dashboard)
    task_form = TaskForm()
    mission_form = MissionForm()
    project_form = ProjectForm()
    inventory_form = InventoryForm(instance=inventory)

    context = {
        'user_profile': user_profile,
        'tasks': tasks,
        'missions': missions,
        'projects': projects,
        'inventory': inventory,
        'task_form': task_form,
        'mission_form': mission_form,
        'project_form': project_form,
        'inventory_form': inventory_form,
    }

    return render(request, 'dashboard.html', context)

# Other view functions as needed for your application

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.shortcuts import render, redirect
from .forms import UserProfileForm
from .models import UserProfile


def register_user(request):
    if request.method == 'POST':
        user_form = CustomUserCreationForm(request.POST)
        if user_form.is_valid():
            user = user_form.save()
            login(request, user)  # Log the user in
            return redirect('update_profile')  # Redirect to profile update page
    else:
        user_form = CustomUserCreationForm()
    return render(request, 'wdmmorpg/register.html', {'user_form': user_form})

@login_required
def update_profile(request):
    try:
        profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        profile = UserProfile(user=request.user)
    
    if request.method == 'POST':
        profile_form = UserProfileForm(request.POST, instance=profile)
        if profile_form.is_valid():
            profile_form.save()
            return redirect('profile_updated')  # Redirect to a confirmation page or somewhere else
    else:
        profile_form = UserProfileForm(instance=profile)
    
    return render(request, 'wdmmorpg/update_profile.html', {'profile_form': profile_form})

@login_required
def user_stats_view(request):
    user_profile = UserProfile.objects.get(user=request.user)
    context = {
        'user_profile': user_profile,
    }
    return render(request, 'wdmmorpg/user_stats.html', context)  # Use the template you created
