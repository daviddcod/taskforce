from django.db import models
# Create your models here.
import datetime
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from mutagen.mp3 import MP3
from mutagen.wave import WAVE
import os
from django.conf import settings
from plan_selection.models import Plan


# User Profile with Level, Experience, and Attributes
class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    selected_plan = models.ForeignKey(Plan, on_delete=models.SET_NULL, null=True)
    level = models.IntegerField(default=1)
    experience = models.IntegerField(default=0)
    prestige = models.IntegerField(default=0)
    health = models.IntegerField(default=100)
    endurance = models.IntegerField(default=100)
    mind = models.IntegerField(default=100)

    def get_role(self):
        if self.level <= 16:
            return 'visitor'
        elif 17 <= self.level <= 36:
            return 'traverser'
        elif self.level >= 37:
            return 'administrator'
        else:
            return 'undefined'

    def add_experience(self, exp):
        self.experience += exp
        self.check_level_up()
        self.save()

    def check_level_up(self):
        required_exp = self.calculate_exp_for_next_level()
        while self.experience >= required_exp:
            self.level_up()
            required_exp = self.calculate_exp_for_next_level()
        if self.level > 100:
            self.prestige += 1
            self.level = 1

    def calculate_exp_for_next_level(self):
        if self.level <= 16:
            return 100 * self.level
        elif self.level <= 36:
            return 200 * self.level
        else:
            return 500 * self.level

    def level_up(self):
        self.level += 1
        self.experience -= self.calculate_exp_for_next_level()

# Rank and Priority Scale
class Rank(models.Model):
    title = models.CharField(max_length=100)
    points = models.IntegerField()

    def __str__(self):
        return self.title

class PriorityScale(models.Model):
    title = models.CharField(max_length=100)
    rank = models.ForeignKey(Rank, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

# Environment Model
class Environment(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    location = models.CharField(max_length=100, null=True)  # Make it nullable temporarily
    users = models.ManyToManyField(settings.AUTH_USER_MODEL)  # Changed to use settings.AUTH_USER_MODEL
    # Rest of the model fields...


    def __str__(self):
        return self.name

# Task, Mission, and Project Models
class Task(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    priority = models.ForeignKey(PriorityScale, on_delete=models.CASCADE)
    environment = models.ForeignKey(Environment, on_delete=models.CASCADE)
    due_date = models.DateField(null=True, blank=True)  # Added this line
    status = models.CharField(max_length=100, null=True, blank=True)  # Added this line
    is_active = models.BooleanField(default=True)
    is_completed = models.BooleanField(default=False)
    # Rest of your fields...
    
    def __str__(self):
        return self.title


    def calculate_experience(self):
        return self.priority.rank.points * 10

class Mission(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    priority = models.ForeignKey(PriorityScale, on_delete=models.CASCADE)
    tasks = models.ManyToManyField(Task)

    def calculate_experience(self):
        return sum([task.calculate_experience() for task in self.tasks.all()]) * 1.2

class Project(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    missions = models.ManyToManyField(Mission)
    start_date = models.DateField(null=True, blank=True)  # Added this field
    end_date = models.DateField(null=True, blank=True)    # Added this field
    status = models.CharField(max_length=100, null=True, blank=True)  # Added this line

    def calculate_experience(self):
        return sum([mission.calculate_experience() for mission in self.missions.all()]) * 1.5

class TransportationKey(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    type = models.CharField(max_length=100, default='public')
    access_level = models.CharField(max_length=100, default='Standard')
    # Other fields...

class Consumable(models.Model):
    name = models.CharField(max_length=100)
    material = models.CharField(max_length=100)
    effect = models.IntegerField(default=0)  # Add a default value here
    # Assuming duration is an integer representing time in minutes (or any other unit you prefer)
    duration = models.IntegerField(default=0)  # Add a default value here

    def __str__(self):
        return f"{self.name} ({self.material})"

class Tool(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    quality = models.CharField(max_length=100, default='Standard')
    type = models.CharField(max_length=100, default='digital')
    # Rest of the model fields...

class Inventory(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    tools = models.ManyToManyField(Tool, blank=True)
    transportation_keys = models.ManyToManyField(TransportationKey, blank=True)
    consumables = models.ManyToManyField(Consumable, blank=True)

# Task Player Functionality
class TaskPlayer(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True, blank=True, default=datetime.datetime(2024, 12, 31, 23, 59, 59))
    achievements = models.JSONField(default=dict)

    def start_task(self):
        self.start_time = timezone.now()
        self.save()

    def end_task(self):
        self.end_time = timezone.now()
        self.user.add_experience(self.task.calculate_experience())
        self.save()

    def add_achievement(self, achievement_name, value):
        self.achievements[achievement_name] = self.achievements.get(achievement_name, 0) + value
        self.save()

    @property
    def duration(self):
        if self.end_time:
            return (self.end_time - self.start_time).total_seconds()
        return (timezone.now() - self.start_time).total_seconds()

    def __str__(self):
        return f"{self.user.user.username} - {self.task.title}"

# InventoryItem Model
class InventoryItem(models.Model):
    name = models.CharField(max_length=100)
    item_type = models.CharField(max_length=100)
    quantity = models.IntegerField(default=0)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

# Skill Model
class Skill(models.Model):
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=100)
    level = models.IntegerField(default=1)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

# UserTaskInteraction Model
class UserTaskInteraction(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(null=True, blank=True, default=datetime.datetime(2024, 12, 31, 23, 59, 59))
    achievements = models.JSONField(default=dict)

    def __str__(self):
        return f"{self.user.user.username} - {self.task.title}"
