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
    tasks = Task.objects.filter(environment__user=user_profile, user=request.user) 
    missions = Mission.objects.filter(tasks__environment__user=user_profile, user=request.user) 
    projects = Project.objects.filter(missions__tasks__environment__user=user_profile, user=request.user)
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
            # Save the new user object
            user = user_form.save()

            # Create a new UserProfile instance and link it to the new user
            UserProfile.objects.create(user=user)  # Adjust if you have additional fields

            # Log the user in
            login(request, user)

            # Redirect to profile update page or a welcome page where they can create their first project
            return redirect('wdm:update_profile')
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

@login_required
def task_list(request):
    tasks = Task.objects.filter(user=request.user.userprofile)
    return render(request, 'wdmmorpg/tasklist.html', {'tasks': tasks})

@login_required
def task_detail(request, pk):
    print("pk:", pk)  # Add this line for debugging
    print(request.user.userprofile)
    task = Task.objects.get(id=pk)  # Use get instead of filter to ensure only one task is returned
    return render(request, 'wdmmorpg/task_detail.html', {'task': task})


from .forms import TaskForm
from django.shortcuts import redirect

@login_required
def task_create(request):
    if request.method == 'POST':
        form = TaskForm(request.POST, user= request.user.userprofile)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user.userprofile
            task.save()
            return redirect('wdmmorpg:task_list')
    else:
        form = TaskForm(user=request.user.userprofile)
    return render(request, 'wdmmorpg/task_form.html', {'form': form})

from django.http import HttpResponseNotFound
@login_required
def task_update(request, pk):
    task = Task.objects.filter(user=request.user.userprofile, id=pk).first()
    if task is None:
        # Handle the case where the task doesn't exist or doesn't belong to the user
        return HttpResponseNotFound("Task not found")

    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('wdm:task_detail', pk=task.pk)
    else:
        form = TaskForm(instance=task)
    return render(request, 'wdmmorpg/task_form.html', {'form': form})


from django.shortcuts import redirect

@login_required
def task_delete(request, pk):
    Task.objects.filter(user=request.user.userprofile, id=pk).delete()
    return redirect('wdm:task_list')
from django.shortcuts import render, get_object_or_404, redirect
from .forms import EnvironmentForm

@login_required
def add_environment(request):
    if request.method == 'POST':
        form = EnvironmentForm(request.POST, user=request.user)
        if form.is_valid():
            form.save()
            return redirect('wdm:envlist')  # Redirect to the list of environments after creation
    else:
        form = EnvironmentForm(user=request.user)
    return render(request, 'wdmmorpg/addenv.html', {'form': form})

@login_required
def environment_list(request):
    environments = Environment.objects.filter(user=request.user.userprofile)
    return render(request, 'wdmmorpg/envlist.html', {'environments': environments})

@login_required
def update_environment(request, pk):
    environment = get_object_or_404(Environment, pk=pk, user=request.user.userprofile)
    if request.method == 'POST':
        form = EnvironmentForm(request.POST, instance=environment)
        if form.is_valid():
            form.save()
            return redirect('wdm:envlist')
    else:
        form = EnvironmentForm(instance=environment)
    return render(request, 'wdmmorpg/edit_environment.html', {'form': form})

@login_required
def delete_environment(request, pk):
    environment = get_object_or_404(Environment, pk=pk, user=request.user.userprofile)
    if request.method == 'POST':
        environment.delete()
        return redirect('wdm:envlist')
    return render(request, 'wdmmorpg/delete_environment.html', {'environment': environment})

@login_required
def update_environment(request, pk):
    environment = get_object_or_404(Environment, pk=pk, user=request.user.userprofile)
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
@login_required
def create_priorityscale(request):
    if request.method == "POST":
        form = PriorityScaleForm(request.POST, user=request.user.userprofile)
        if form.is_valid():
            priorityscale = form.save(commit=False)
            priorityscale.user = request.user.userprofile
            priorityscale.save()
            return redirect('wdm:priorityscale_list')
    else:
        form = PriorityScaleForm(user=request.user.userprofile)
    return render(request, 'wdmmorpg/priorityscale_form.html', {'form': form})

# Read
@login_required
def list_priorityscale(request):
    priorityscales = PriorityScale.objects.filter(user=request.user.userprofile)
    return render(request, 'wdmmorpg/list_priorityscale.html', {'priorityscales': priorityscales})

# Update
@login_required
def update_priorityscale(request, pk):
    priorityscale = get_object_or_404(PriorityScale, pk=pk, user=request.user.userprofile)
    if request.method == "POST":
        form = PriorityScaleForm(request.POST, instance=priorityscale)
        if form.is_valid():
            form.save()
            return redirect('wdm:priorityscale_list')
    else:
        form = PriorityScaleForm(instance=priorityscale)
    return render(request, 'wdmmorpg/priorityscale_form.html', {'form': form})

# Delete
@login_required
def delete_priorityscale(request, pk):
    PriorityScale.objects.filter(id=pk, user=request.user.userprofile).delete()
    return redirect('wdm:priorityscale_list')

# views.py
from django.shortcuts import render, get_object_or_404, redirect
from .forms import RankForm
from .models import Rank

# Create a new Rank
@login_required
def create_rank(request):
    if request.method == 'POST':
        form = RankForm(request.POST)
        if form.is_valid():
            rank = form.save(commit=False)
            rank.user = request.user.userprofile
            rank.save()
            return redirect('wdm:rank_list')
    else:
        form = RankForm()
    return render(request, 'wdmmorpg/rank_form.html', {'form': form})

# List all Ranks
@login_required
def list_rank(request):
    ranks = Rank.objects.filter(user=request.user.userprofile)
    return render(request, 'wdmmorpg/rank_list.html', {'ranks': ranks})

# Update a specific Rank
@login_required
def update_rank(request, pk):
    rank = get_object_or_404(Rank, pk=pk, user=request.user.userprofile)
    if request.method == 'POST':
        form = RankForm(request.POST, instance=rank)
        if form.is_valid():
            form.save()
            return redirect('wdm:rank_list')
    else:
        form = RankForm(instance=rank)
    return render(request, 'wdmmorpg/rank_form.html', {'form': form})

# Delete a specific Rank
@login_required
def delete_rank(request, pk):
    Rank.objects.filter(id=pk, user=request.user.userprofile).delete()
    return redirect('wdm:rank_list')

from django.http import HttpResponse

from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import UserProfileForm

@login_required
def profile_create(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            return redirect('wdm:profile_success')
    else:
        form = UserProfileForm()
    return render(request, 'wdmmorpg/profile_create.html', {'form': form})

def profile_success(request):
    return HttpResponse('Profile successfully created!')

from django.shortcuts import render, redirect
from .forms import MissionForm
from .models import Mission

@login_required
def create_mission(request):
    if request.method == 'POST':
        form = MissionForm(request.POST, user=request.user.userprofile)  # Pass the user and POST data to the form
        form.set_userprofile(request.user.userprofile)  # Updated method name to match MissionForm

        if form.is_valid():
            mission = form.save(commit=False)
            mission.user = request.user.userprofile  # Assign the current user to the mission
            mission.save()
            form.save_m2m()
            return redirect('wdm:mission_list')  # Redirect to the list view after creating
    else:
        form = MissionForm()  # Create the form without the 'user' argument
        form.set_userprofile(request.user.userprofile)  # Updated method name to match MissionForm

    # Call set_user method here to set the queryset for tasks

    return render(request, 'wdmmorpg/mission_form.html', {'form': form})

@login_required
def mission_detail(request, pk):
    mission = get_object_or_404(Mission, pk=pk, user=request.user.userprofile)
    tasks = mission.tasks.filter(user=request.user.userprofile)
    context = {
        'mission': mission,
        'tasks': tasks
    }
    return render(request, 'wdmmorpg/mission_detail.html', context)

from django.db import transaction
@login_required
def update_mission(request, pk):
    mission = get_object_or_404(Mission, pk=pk, user=request.user.userprofile)

    if request.method == 'POST':
        form = MissionForm(request.POST, instance=mission, user=request.user)  # Pass the user and POST data to the form
        form.set_userprofile(request.user.userprofile, pk)  # Updated method name to match MissionForm

        if form.is_valid():
            with transaction.atomic():  # Use a transaction to ensure atomicity
                mission = form.save(commit=False)
                mission.user = request.user.userprofile
                mission.save()
                form.save_m2m()

                # Clear existing tasks and add the selected ones
                existing_tasks = set(mission.tasks.all())
                selected_tasks = set(form.cleaned_data['tasks'])
                # Remove tasks no longer selected
                for task in existing_tasks - selected_tasks:
                    mission.tasks.remove(task)
                # Add new tasks
                for task in selected_tasks - existing_tasks:
                    mission.tasks.add(task)

            return redirect('wdm:mission_list')
    else:
        form = MissionForm(instance=mission, user=request.user)  # Pass the user to the form for GET request
        form.set_userprofile(request.user.userprofile, pk)
    return render(request, 'wdmmorpg/mission_form.html', {'form': form})

from django.views.decorators.http import require_POST

@require_POST  # Ensures this view can only be accessed via POST request
def delete_mission(request, pk):
    mission = get_object_or_404(Mission, pk=pk)
    mission.delete()
    return redirect('wdm:mission_list')  # Redirect to the list view after deleting

def mission_list(request):
    missions = Mission.objects.filter(user=request.user.userprofile)
    return render(request, 'wdmmorpg/mission_list.html', {'missions': missions})

from django.shortcuts import render, redirect
from .forms import ProjectForm
from django.contrib.auth.decorators import login_required

@login_required
def create_project(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)  # Pass the user to the form
        form.set_user(request.user)

        if form.is_valid():
            # Create a new project instance without saving it to the DB yet
            new_project = form.save(commit=False)
            new_project.user = request.user.userprofile  # Assign the current user's profile to the project
            new_project.save()  # Save the project to the DB
            form.save_m2m()  # If the form has many-to-many fields, this is required
            return redirect('wdm:project_list')  # Redirect to the list view
    else:
        form = ProjectForm()  # Pass the user to the form
        form.set_user(request.user)

    return render(request, 'wdmmorpg/create_project.html', {'form': form})

from django.contrib.auth.decorators import login_required

@login_required
def update_project(request, project_id):
    # Ensure the project belongs to the user
    project = get_object_or_404(Project, pk=project_id, user=request.user.userprofile)
    
    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            updated_project = form.save()
            # Assuming missions are user-specific as well
            mission_ids = request.POST.getlist('missions')
            updated_project.missions.set(Mission.objects.filter(id__in=mission_ids, user=request.user.userprofile))
            return redirect('wdm:project_detail', pk=updated_project.id)
    else:
        form = ProjectForm(instance=project)
    return render(request, 'wdmmorpg/update_project.html', {'form': form, 'project': project})

@login_required
def delete_project(request, pk):
    # Ensure the project belongs to the user
    project = get_object_or_404(Project, pk=pk, user=request.user.userprofile)
    if request.method == 'POST':
        project.delete()
        return redirect('wdm:project_list')
    return render(request, 'wdmmorpg/delete_project.html', {'project': project})

@login_required
def project_detail(request, pk):
    # Ensure the project belonags to the user
    project = get_object_or_404(Project, pk=pk, user=request.user.userprofile)
    mission = project.missions.filter(user=request.user.userprofile).first()  # Replace 'missions' with related_name if set
    experience = mission.calculate_experience() if mission else 0
    return render(request, 'wdmmorpg/project_detail.html', {
        'project': project,
        'mission': mission,
        'experience': experience
    })

from django.shortcuts import render
from .models import Project

@login_required
def project_list(request):
    # Retrieve only projects belonging to the user
    projects = Project.objects.filter(user=request.user.userprofile)
    return render(request, 'wdmmorpg/project_list.html', {'projects': projects})

def completed_tasks(request):
    completed_tasks = Task.objects.filter(is_completed=True)
    return render(request, 'wdmmorpg/task_completion.html', {'completed_tasks': completed_tasks})

from django.shortcuts import get_object_or_404, redirect
from django.utils.timezone import now
from .models import Task, Project, UserProfile
@login_required
def complete_task(request, task_id):
    # Get the task and project or return a 404 error if not found
    task = get_object_or_404(Task, pk=task_id)
    pk = task_id

    # Check if the task is already completed
    if not task.is_completed:
        # Mark the task as completed
        task.is_completed = True
        task.status = 'Completed'
        task.completed_on = str(now())  # Assign the completion time to the variable
        task.is_active = False

        # Calculate and assign the gained experience from completing the task
        # Load priority and rank models before calculating
        gained_experience = task.calculate_experience()
        task.experience_gained = gained_experience
        # Save the changes to the task
        task.save()

        # Update the user's experience in their profile using the model's method
        user_profile, created = UserProfile.objects.get_or_create(user=request.user)
        user_profile.add_experience(gained_experience)


        # Since we've marked the task as completed, it's removed from the active task list automatically.
        # There's no need to manually remove it from the project's tasks as it's handled by the task's is_completed attribute.

        # Redirect to the task detail or another appropriate page
        return redirect('wdm:objective_overview')

    # If the task is already completed, redirect to the task list or appropriate page
    return redirect('wdm:objective_overview')


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

@login_required
def user_profile(request):
    # Fetch the UserProfile for the currently logged-in user
    profile = get_object_or_404(UserProfile, user=request.user)
    experience_percentage = profile.calculate_experience_percentage()
    next_level = profile.level + 1
    return render(request, 'wdmmorpg/user_profile.html', {'profile': profile, 'experience_percentage': experience_percentage, 'next_level': next_level})

# wdmmorpg/views.py

from django.shortcuts import render
from .models import UserProfile, Rank, PriorityScale, Task, Mission, Project, Environment

from django.shortcuts import get_object_or_404
from django.shortcuts import render, get_object_or_404
from .models import UserProfile, Project, Mission, Task, Rank, PriorityScale

def objective_overview(request, project_id=None):
    user_profile = request.user.userprofile
    projects = Project.objects.filter(user=user_profile)
    missions = Mission.objects.filter(user=user_profile)
    tasks = Task.objects.filter(user=user_profile)
    ranks = Rank.objects.filter(user=user_profile)
    priority_scales = PriorityScale.objects.filter(user=user_profile)

    # If no user-specific ranks or priority scales, use defaults
    if not ranks.exists():
        ranks = Rank.objects.filter(user__isnull=True)
    if not priority_scales.exists():
        priority_scales = PriorityScale.objects.filter(user__isnull=True)

    # Use user's priority scales if they exist, otherwise use default
    priority_scales = PriorityScale.objects.filter(user=user_profile)
    if not priority_scales.exists():
        priority_scales = PriorityScale.objects.filter(user__isnull=True)  # Assuming a default set

    selected_project = None
    if project_id:
        selected_project = get_object_or_404(Project, id=project_id, user=user_profile)
        missions = missions.filter(project=selected_project)
        tasks = tasks.filter(mission__in=missions)  # Filter tasks based on the filtered missions

    context = {
        'projects': projects,
        'missions': missions,
        'tasks': tasks,
        'selected_project': selected_project,
        'ranks': ranks,
        'priority_scales': priority_scales,
    }

    print('Projects:', projects)
    print('Missions:', missions)
    print('Tasks:', tasks)
    print('Ranks:', ranks)
    print('Priority Scales:', priority_scales)

    return render(request, 'wdmmorpg/objective_overview.html', context)


