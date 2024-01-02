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
    priority = forms.ModelChoiceField(
        label='Priority',
        queryset=PriorityScale.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    tasks = forms.ModelMultipleChoiceField(
        label='Tasks',
        queryset=Task.objects.none(),
        widget=forms.CheckboxSelectMultiple,
        required=False
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


    def set_user(self, user):
        tasks_queryset = Task.objects.filter(user=user).order_by('your_field_to_order_by')
        self.fields['tasks'].queryset = tasks_queryset
        
    @transaction.atomic
    def save(self, commit=True):
        mission = super().save(commit=False)
        if commit:
            mission.save()
            self.save_m2m()
        return mission

    def set_user(self, user):
        self.fields['tasks'].queryset = Task.objects.filter(user=user.userprofile)
        
    def __init__(self, *args, **kwargs):
        mission = kwargs.get('instance')
        self.user = kwargs.pop('user', None)
        super(MissionForm, self).__init__(*args, **kwargs)
        if mission and hasattr(mission, 'user'):
            self.set_user(mission.user)
        elif self.user:
            self.set_user(self.user)
        else:
            self.fields['tasks'].queryset = Task.objects.none()
# ProjectForm
class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'description', 'start_date', 'end_date', 'status', 'missions']

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')
        if start_date and end_date and end_date < start_date:
            raise ValidationError('End date must be after start date.')
        return cleaned_data

    def set_user(self, user):
        self.fields['missions'].queryset = Mission.objects.filter(user=user.userprofile)
        
    @transaction.atomic
    def save(self, commit=True):
        project = super().save(commit=False)
        if commit:
            project.save()
            self.save_m2m()
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
    class Meta:
        model = Environment
        fields = ['name', 'location', 'description', 'users']

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
        fields = ['task', 'user', 'end_time', 'achievements']

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
            task = self.cleaned_data['task']
            user_profile = self.cleaned_data['player']
            user_profile.experience += calculate_exp_for_task(task.priority)
            user_profile.save()
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
