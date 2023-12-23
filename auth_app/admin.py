from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

# Assuming .models refers to the same file that contains CustomUser
from .models import CustomUser

# Define a new User admin
class UserAdmin(BaseUserAdmin):
    list_display = ('id', 'username', 'email', 'first_name', 'last_name', 'is_staff')
    # Add or remove fields as you need

# Re-register UserAdmin
# Make sure CustomUser is the name of your custom user model
admin.site.register(CustomUser, UserAdmin)
