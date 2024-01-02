from django.shortcuts import render, redirect
from .models import UserProfile, Task, Mission, Project, Inventory, Tool, TransportationKey, Consumable, Environment
from .forms import TaskForm, MissionForm, ProjectForm, InventoryForm, UserProfileForm, UserProfile, UserTaskInteraction, UserTaskInteractionForm, CustomUserCreationForm
from django.contrib.auth.decorators import login_required
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import UserProfile, Task, Mission, Project, Inventory, Plan  # Import the Plan model
from .forms import TaskForm, MissionForm, ProjectForm, InventoryForm
from django.shortcuts import get_object_or_404
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
            return redirect('wdm:update_profile')  # Redirect to profile update page
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
            return redirect('wdm:profile_updated')  # Redirect to a confirmation page or somewhere else
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

from django.shortcuts import render
from .models import Task

def task_list(request):
    tasks = Task.objects.all()
    return render(request, 'wdmmorpg/tasklist.html', {'tasks': tasks})

def task_detail(request, pk):
    task = Task.objects.get(id=pk)
    return render(request, 'wdmmorpg/task_detail.html', {'task': task})

from .forms import TaskForm
from django.shortcuts import redirect

def task_create(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('wdmmorpg:task_list')
    else:
        form = TaskForm()
    return render(request, 'wdmmorpg/task_form.html', {'form': form})

def task_update(request, pk):
    task = Task.objects.get(id=pk)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('wdm:task_detail', pk=task.pk)
    else:
        form = TaskForm(instance=task)
    return render(request, 'wdmmorpg/task_form.html', {'form': form})

from django.shortcuts import redirect

def task_delete(request, pk):
    Task.objects.get(id=pk).delete()
    return redirect('wdm:task_list')

# views.py
from django.shortcuts import render, redirect
from .forms import EnvironmentForm

def add_environment(request):
    if request.method == 'POST':
        form = EnvironmentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('wdm:envlist')  # Redirect to the list of environments after creation
    else:
        form = EnvironmentForm()
    return render(request, 'wdmmorpg/addenv.html', {'form': form})

def environment_list(request):
    environments = Environment.objects.all()  # Retrieve all environments from the database
    return render(request, 'wdmmorpg/envlist.html', {'environments': environments})

def update_environment(request, pk):
    environment = get_object_or_404(Environment, pk=pk)
    if request.method == 'POST':
        form = EnvironmentForm(request.POST, instance=environment)
        if form.is_valid():
            form.save()
            return redirect('wdm:envlist')
    else:
        form = EnvironmentForm(instance=environment)
    return render(request, 'wdmmorpg/edit_environment.html', {'form': form})

def delete_environment(request, pk):
    environment = get_object_or_404(Environment, pk=pk)
    if request.method == 'POST':
        environment.delete()
        return redirect('wdm:envlist')
    return render(request, 'wdmmorpg/delete_environment.html', {'environment': environment})

def update_environment(request, pk):
    environment = get_object_or_404(Environment, pk=pk)
    if request.method == 'POST':
        form = EnvironmentForm(request.POST, instance=environment)
        if form.is_valid():
            form.save()
            return redirect('wdm:envlist')
    else:
        form = EnvironmentForm(instance=environment)
    return render(request, 'wdmmorpg/update_environment.html', {'form': form})

from .forms import PriorityScaleForm
from .models import PriorityScale

# Create
def create_priorityscale(request):
    if request.method == "POST":
        form = PriorityScaleForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('wdm:priorityscale_list')
    else:
        form = PriorityScaleForm()
    return render(request, 'wdmmorpg/priorityscale_form.html', {'form': form})

# Read
def list_priorityscale(request):
    priorityscales = PriorityScale.objects.all()
    return render(request, 'wdmmorpg/list_priorityscale.html', {'priorityscales': priorityscales})

# Update
def update_priorityscale(request, pk):
    priorityscale = get_object_or_404(PriorityScale, pk=pk)
    if request.method == "POST":
        form = PriorityScaleForm(request.POST, instance=priorityscale)
        if form.is_valid():
            form.save()
            return redirect('wdm:priorityscale_list')
    else:
        form = PriorityScaleForm(instance=priorityscale)
    return render(request, 'wdmmorpg/priorityscale_form.html', {'form': form})

# Delete
def delete_priorityscale(request, pk):
    PriorityScale.objects.filter(id=pk).delete()
    return redirect('wdm:priorityscale_list')

# views.py
from django.shortcuts import render, get_object_or_404, redirect
from .forms import RankForm
from .models import Rank

# Create a new Rank
def create_rank(request):
    if request.method == 'POST':
        form = RankForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('wdm:rank_list')
    else:
        form = RankForm()
    return render(request, 'wdmmorpg/rank_form.html', {'form': form})

# List all Ranks
def list_rank(request):
    ranks = Rank.objects.all()
    return render(request, 'wdmmorpg/rank_list.html', {'ranks': ranks})

# Update a specific Rank
def update_rank(request, pk):
    rank = get_object_or_404(Rank, pk=pk)
    if request.method == 'POST':
        form = RankForm(request.POST, instance=rank)
        if form.is_valid():
            form.save()
            return redirect('wdm:rank_list')
    else:
        form = RankForm(instance=rank)
    return render(request, 'wdmmorpg/rank_form.html', {'form': form})

# Delete a specific Rank
def delete_rank(request, pk):
    Rank.objects.filter(id=pk).delete()
    return redirect('wdm:rank_list')

from django.http import HttpResponse

from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import UserProfileForm

def profile_create(request):
    if not request.user.is_authenticated:  # Check if the user is authenticated
        return redirect('auth_app:login')  # Redirect to login page or wherever you handle authentication

    if request.method == 'POST':
        form = UserProfileForm(request.POST)
        if form.is_valid():
            profile = form.save(commit=False)  # Don't save the form immediately
            profile.user = request.user  # Assign the logged-in user
            profile.save()  # Save the UserProfile instance
            return redirect('wdm:profile_success')
    else:
        form = UserProfileForm()

    return render(request, 'wdmmorpg/profile_create.html', {'form': form})
def profile_success(request):
    return HttpResponse('Profile successfully created!')

    from django.shortcuts import render, redirect
from .forms import MissionForm
from .models import Mission

def create_mission(request):
    if request.method == 'POST':
        form = MissionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('wdm:mission_list')  # Redirect to the list view after creating
    else:
        form = MissionForm()
    return render(request, 'wdmmorpg/mission_form.html', {'form': form})

from django.shortcuts import render, get_object_or_404
from .models import Mission  # Ensure you're importing the Mission model

def mission_detail(request, pk):
    # Fetch the mission by primary key or return 404 if not found
    mission = get_object_or_404(Mission, pk=pk)

    # If you have a reverse relationship set up (like a ForeignKey from Task to Mission),
    # Django automatically creates a manager on the Mission model for related tasks.
    # You can access it via 'mission.task_set.all()' if your model is named 'Task'.
    # For a ManyToManyField, you can directly access 'mission.tasks.all()'.
    # Assuming it's a ManyToManyField as per your initial setup:
    tasks = mission.tasks.all()

    # Pass both the mission and its related tasks to the template context.
    context = {
        'mission': mission,
        'tasks': tasks  # Add the tasks to the context
    }
    return render(request, 'wdmmorpg/mission_detail.html', context)

def update_mission(request, pk):
    mission = get_object_or_404(Mission, pk=pk)
    if request.method == 'POST':
        form = MissionForm(request.POST, instance=mission)
        if form.is_valid():
            form.save()
            return redirect('wdm:mission_detail', pk=mission.pk)  # Redirect to the detail view
    else:
        form = MissionForm(instance=mission)
    return render(request, 'wdmmorpg/mission_form.html', {'form': form})

from django.views.decorators.http import require_POST

@require_POST  # Ensures this view can only be accessed via POST request
def delete_mission(request, pk):
    mission = get_object_or_404(Mission, pk=pk)
    mission.delete()
    return redirect('wdm:mission_list')  # Redirect to the list view after deleting

def mission_list(request):
    missions = Mission.objects.all()
    return render(request, 'wdmmorpg/mission_list.html', {'missions': missions})

from django.shortcuts import render, redirect
from .forms import ProjectForm

def create_project(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('wdm:project_list')  # Redirect to the list view
    else:
        form = ProjectForm()
    return render(request, 'wdmmorpg/create_project.html', {'form': form})

from django.contrib.auth.decorators import login_required

@login_required
def update_project(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    
    if request.method == 'POST':
        # Process the form data
        form = ProjectForm(request.POST, instance=project)  # Assuming you have a ProjectForm

        if form.is_valid():
            updated_project = form.save()

            # Update missions associations
            mission_ids = request.POST.getlist('missions')
            updated_project.missions.set(Mission.objects.filter(id__in=mission_ids))

            # Redirect to a success page, project detail or list
            return redirect('wdm:project_detail', project_id=updated_project.id)
    
    else:
        # If not POST, instantiate the form with the current project instance
        form = ProjectForm(instance=project)
    
    # Assuming you pass 'all_missions' to the template context
    return redirect('wdm:project_detail', pk=project_id)

def delete_project(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if request.method == 'POST':
        project.delete()
        return redirect('wdm:project_list')
    return render(request, 'wdmmorpg/delete_project.html', {'project': project})

def project_detail(request, pk):
    project = get_object_or_404(Project, pk=pk)
    # Assuming the Project model has a OneToOneField or ForeignKey to Mission
    mission = project.missions.first()  # Replace 'mission_set' with related_name if set
    # Calculate experience if needed, or you can do this in the template with mission.calculate_experience
    experience = mission.calculate_experience() if mission else 0
    return render(request, 'wdmmorpg/project_detail.html', {
        'project': project,
        'mission': mission,
        'experience': experience
    })
from django.shortcuts import render
from .models import Project

def project_list(request):
    projects = Project.objects.all()  # Retrieve all projects from the database
    return render(request, 'wdmmorpg/project_list.html', {'projects': projects})

def completed_tasks(request):
    completed_tasks = Task.objects.filter(is_completed=True)
    return render(request, 'wdmmorpg/task_completion.html', {'completed_tasks': completed_tasks})

@login_required
def complete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    if not task.is_completed:
        task.is_completed = True
        task.status = 'Completed on ' + str(datetime.now())
        task.is_active = False
        gained_experience = task.calculate_experience()
        task.save()

        # Update user experience
        user_profile = UserProfile.objects.get(user=request.user)
        user_profile.experience += gained_experience
        user_profile.save()

        # Redirect to the task detail or another appropriate page
        return redirect('wdm:task_detail', task_id=task_id)
    return redirect('wdm:task_list')

@login_required
def add_missions_to_project(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    if request.method == 'POST':
        mission_ids = request.POST.getlist('missions')  # Get list of mission ids
        missions = Mission.objects.filter(id__in=mission_ids)
        for mission in missions:
            project.missions.add(mission)  # Add each mission to the project
        project.save()
        return redirect('wdm:project_detail', project_id=project_id)
    return redirect('wdm:project_list')  # Redirect to a list of projects or an appropriate view