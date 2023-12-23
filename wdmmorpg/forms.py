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
        fields = ['title', 'description', 'priority', 'environment']

    def clean_due_date(self):
        due_date = self.cleaned_data['due_date']
        if due_date and due_date < date.today():
            raise ValidationError('Due date cannot be in the past.')
        return due_date

    # Additional custom validations

# MissionForm
class MissionForm(forms.ModelForm):
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

    @transaction.atomic
    def save(self, commit=True):
        mission = super().save(commit=False)
        if commit:
            mission.save()
            self.save_m2m()
        return mission

    # Additional custom validations

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
    # Add additional fields here
    level = forms.IntegerField()
    experience = forms.IntegerField()
    prestige = forms.IntegerField()
    health = forms.IntegerField()
    endurance = forms.IntegerField()
    mind = forms.IntegerField()
    
    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('email',)  # Add additional fields if needed

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            # Now save the UserProfile fields
            UserProfile.objects.create(
                user=user,
                level=self.cleaned_data['level'],
                experience=self.cleaned_data['experience'],
                prestige=self.cleaned_data['prestige'],
                health=self.cleaned_data['health'],
                endurance=self.cleaned_data['endurance'],
                mind=self.cleaned_data['mind'],
            )
        return user
