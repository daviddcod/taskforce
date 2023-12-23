from django.contrib import admin
from .models import UserProfile, Task, Mission, Project, InventoryItem, \
                    Environment, Tool, TransportationKey, Consumable, \
                    Skill, PriorityScale, Rank, TaskPlayer, Inventory, UserTaskInteraction

# Register your models here.
admin.site.register(UserProfile)
admin.site.register(Task)
admin.site.register(Mission)
admin.site.register(Project)
admin.site.register(InventoryItem)
admin.site.register(Environment)
admin.site.register(Tool)
admin.site.register(TransportationKey)
admin.site.register(Consumable)
admin.site.register(Skill)
admin.site.register(PriorityScale)
admin.site.register(Rank)
admin.site.register(TaskPlayer)
admin.site.register(Inventory)
admin.site.register(UserTaskInteraction)
