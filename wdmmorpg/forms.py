from django import forms
from django.core.exceptions import ValidationError
from django.db import transaction
from django.utils import timezone
from datetime import date

#to implement: InventoryItem, Skill, TaskP

from .models import (UserProfile, Task, Mission, Project, InventoryItem, 
                     Environment, Tool, TransportationKey, Consumable, 
                     Skill, PriorityScale, Rank, TaskPlayer, Inventory, UserTaskInteraction)

# UserTaskInteractionForm
class UserTaskInteractionForm(forms.ModelForm):
    class Meta:
        model = UserTaskInteraction
        fields = ['user', 'task', 'end_time', 'achievements']

    def clean_end_time(self):
        end_time = self.cleaned_data.get('end_time')
        if end_time and end_time < timezone.now():
            raise ValidationError('End time cannot be in the past.')
        return end_time

# ToolForm
class ToolForm(forms.ModelForm):
    class Meta:
        model = Tool
        fields = ['name', 'description']

# TransportationKeyForm
class TransportationKeyForm(forms.ModelForm):
    class Meta:
        model = TransportationKey
        fields = ['name', 'description']

# ConsumableForm
class ConsumableForm(forms.ModelForm):
    class Meta:
        model = Consumable
        fields = ['name', 'material']

# InventoryForm
class InventoryForm(forms.ModelForm):
    class Meta:
        model = Inventory
        fields = ['user', 'tools', 'transportation_keys', 'consumables']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['tools'].queryset = Tool.objects.all()
        self.fields['transportation_keys'].queryset = TransportationKey.objects.all()
        self.fields['consumables'].queryset = Consumable.objects.all()

    @transaction.atomic
    def save(self, commit=True):
        inventory = super().save(commit=False)
        if commit:
            inventory.save()
            self.save_m2m()
        return inventory

# Constants
MAX_LEVEL = 100
EXP_THRESHOLD = 1000
PRESTIGE_MAX = 12

def calculate_exp_for_task(priority):
    # Example logic for experience calculation based on task priority
    return priority.points * 10

# UserProfileForm
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['user', 'level', 'experience', 'prestige', 'health', 'endurance', 'mind']
        exclude = ['user'] 
    def clean_level(self):
        level = self.cleaned_data['level']
        if level < 0 or level > MAX_LEVEL:
            raise ValidationError('Level must be between 0 and MAX_LEVEL.')
        return level

    def clean_experience(self):
        experience = self.cleaned_data['experience']
        if experience < 0 or experience > EXP_THRESHOLD:
            raise ValidationError('Experience must be within a valid range.')
        return experience

    def clean_prestige(self):
        prestige = self.cleaned_data['prestige']
        if prestige < 0 or prestige > PRESTIGE_MAX:
            raise ValidationError('Prestige level is not valid.')
        return prestige

    # Additional custom validations

# TaskForm
class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'priority', 'environment', 'is_completed']

    def clean_due_date(self):
        due_date = self.cleaned_data['due_date']
        if due_date and due_date < date.today():
            raise ValidationError('Due date cannot be in the past.')
        return due_date

    # Additional custom validations

# MissionForm

from django import forms
from django.core.exceptions import ValidationError
from django.db import transaction
from .models import Mission, PriorityScale, Task

class MissionForm(forms.ModelForm):
    title = forms.CharField(
        label='Title',
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    description = forms.CharField(
        label='Description',
        widget=forms.Textarea(attrs={'class': 'form-control'})
    )
    tasks = forms.ModelMultipleChoiceField(
        label='Tasks',
        queryset=Task.objects.none(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    priority = forms.ModelChoiceField(
        label='Priority',
        queryset=PriorityScale.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Mission
        fields = ['title', 'description', 'priority', 'tasks']

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')
        if start_date and end_date and end_date < start_date:
            raise ValidationError('End date must be after start date.')
        return cleaned_data

    def set_userprofile(self, user, mission_pk=None):
        if mission_pk:
            tasks_queryset = Task.objects.filter(user=user)
        else:
            tasks_queryset = Task.objects.filter(user=user)
        self.fields['tasks'].queryset = tasks_queryset
        self.fields['priority'] = forms.ModelChoiceField(
        label='Priority',
        queryset=PriorityScale.objects.filter(user=user),
        widget=forms.Select(attrs={'class': 'form-control'})
    )

        
        
    @transaction.atomic
    def save(self, commit=True):
        mission = super().save(commit=False)
        if commit:
            mission.save()
            self.save_m2m()
        return mission

    def __init__(self, *args, **kwargs):
        mission = kwargs.get('instance')
        self.user = kwargs.pop('user', None)
        super(MissionForm, self).__init__(*args, **kwargs)
        if mission:
            # Set tasks queryset for existing mission
            self.set_userprofile(mission.user, mission.id)
        elif self.user:
            # Set tasks queryset for new mission
            self.set_userprofile(self.user)



# ProjectForm
class ProjectForm(forms.ModelForm):
    missions = forms.ModelMultipleChoiceField(
        queryset=Mission.objects.all(),  # Adjust this to your actual queryset
        widget=forms.CheckboxSelectMultiple,
        required=False  # Adjust based on whether a selection is required
    )

    priority = forms.ModelChoiceField(
    label='Priority',
    queryset=PriorityScale.objects.all(),
    widget=forms.Select(attrs={'class': 'form-control'})
    )

    create_taskplayer = forms.BooleanField(
        label='Create a TaskPlayer for this project',
        required=False,
        initial=False
    )

            
    class Meta:
        model = Project
        fields = ['title', 'description', 'priority','start_date', 'end_date', 'status', 'missions', 'create_taskplayer']
        widgets = {
            'end_date': forms.DateInput(attrs={'type': 'date'}),
            'start_date': forms.DateInput(attrs={'type': 'date'}),

        }


    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')
        if start_date and end_date and end_date < start_date:
            raise ValidationError('End date must be after start date.')
        return cleaned_data

    def set_user(self, user):
        self.fields['missions'].queryset = Mission.objects.filter(user=user.userprofile)
        self.fields['priority'].queryset = PriorityScale.objects.filter(user=user.userprofile)
        
    @transaction.atomic
    def save(self, commit=True, user=None):
        project = super().save(commit=False)
        if commit:
            project.save()
            self.save_m2m()

            if self.cleaned_data.get('create_taskplayer'):
                # Retrieve all tasks from the project's missions
                all_tasks = []
                for mission in project.missions.all():
                    for task in mission.tasks.all():
                        all_tasks.append(task)

                # Sort or arrange all_tasks if necessary, then pick the first task as the current_task
                first_task = all_tasks[0] if all_tasks else None

                # Create a new TaskPlayer object
                task_player = TaskPlayer.objects.create(
                    user=project.user,
                    current_task=first_task,  # Set the first task as the current task
                    achievements={'completionist': True},  # Auto-fill achievements
                    project=project,  # Assign the project
                    end_time=project.end_date  # Initialize end_time to the project's end date
                )
                
                print(project.end_date)


                # Add all tasks from the project's missions to the TaskPlayer
                task_player.tasks.set(all_tasks)
                task_player.save()

                # Optionally return both project and task_player
                return project, task_player

        return project

    # Additional custom validations

# InventoryItemForm
class InventoryItemForm(forms.ModelForm):
    class Meta:
        model = InventoryItem
        fields = ['name', 'item_type', 'quantity', 'user']

    def clean_quantity(self):
        quantity = self.cleaned_data['quantity']
        if quantity < 0:
            raise ValidationError('Quantity cannot be negative.')
        return quantity

    # Additional custom validations

# EnvironmentForm
class EnvironmentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(EnvironmentForm, self).__init__(*args, **kwargs)
        if user:
            self.fields['user'].queryset = UserProfile.objects.filter(user=user)

    class Meta:
        model = Environment
        fields = ['name', 'location', 'description', 'user']

    # Custom validations for Environment

# ToolForm
class ToolForm(forms.ModelForm):
    class Meta:
        model = Tool
        fields = ['name', 'type', 'quality']

    # Custom validations for Tool

# TransportationKeyForm
class TransportationKeyForm(forms.ModelForm):
    class Meta:
        model = TransportationKey
        fields = ['name', 'type', 'access_level']

    # Custom validations for TransportationKey

# ConsumableForm
class ConsumableForm(forms.ModelForm):
    class Meta:
        model = Consumable
        fields = ['name', 'material' ,'effect', 'duration']

    # Custom validations for Consumable

# SkillForm
class SkillForm(forms.ModelForm):
    class Meta:
        model = Skill
        fields = ['name', 'type', 'level', 'user']

    # Custom validations for Skill

# PriorityScaleForm
class PriorityScaleForm(forms.ModelForm):
    class Meta:
        model = PriorityScale
        fields = ['title', 'rank']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(PriorityScaleForm, self).__init__(*args, **kwargs)
        if user:
            self.fields['rank'].queryset = Rank.objects.filter(user=user)

    # Custom validations for PriorityScale

# RankForm
class RankForm(forms.ModelForm):
    class Meta:
        model = Rank
        fields = ['title', 'points']

    # Custom validations for Rank

# TaskPlayerForm

class TaskPlayerForm(forms.ModelForm):
    class Meta:
        model = TaskPlayer
        fields = ['tasks', 'user', 'end_time', 'achievements', 'project']

    def clean(self):
        cleaned_data = super().clean()
        start_time = cleaned_data.get('start_time')
        end_time = cleaned_data.get('end_time')
        if start_time and end_time and end_time < start_time:
            raise ValidationError('End time must be after start time.')
        return cleaned_data

    def save(self, commit=True):
        task_player = super().save(commit=False)
        if commit:
            # Experience calculation logic based on task priority
            task = self.cleaned_data['tasks']
            user_profile = self.cleaned_data['user']  # Changed from 'player' to 'user' to match the model field
            project = self.cleaned_data['project']  # Ensure 'project' is included in your form fields

            # Calculate experience and update user profile
            user_profile.experience += calculate_exp_for_task(task.priority)
            user_profile.save()

            # Set the start and end time for TaskPlayer
            task_player.start_time = timezone.now()  # Assuming start_time is set when the task is started
            task_player.end_time = project.end_date  # Set end_time to the end_date of the associated project

            task_player.save()
        return task_player

    
    # Additional custom validations

# Additional forms and custom validations for other models...
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from .models import UserProfile

User = get_user_model()

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email', 'password1', 'password2')  # Only show these fields initially
        help_texts = {
            'username': 'A unique username for your profile.',
            'email': 'We\'ll never share your email with anyone else.',
            # Add more help texts for other fields as needed
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            # Set default values for the extra fields
            UserProfile.objects.create(
                user=user,
                level=1,  # Default level
                experience=0,  # Default experience
                prestige=1,  # Default prestige
                health=200,  # Default health
                endurance=100,  # Default endurance
                mind=75,  # Default mind
            )
        return user


from django import forms
from .models import Task
class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'priority', 'environment', 'due_date', 'status', 'is_active']
        widgets = {
            'due_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(TaskForm, self).__init__(*args, **kwargs)
        if user:
            self.fields['priority'].queryset = PriorityScale.objects.filter(user=user)
            self.fields['environment'].queryset = Environment.objects.filter(user=user)

