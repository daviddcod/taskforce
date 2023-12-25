from django.db import models

# Create your models here.

from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.utils.translation import gettext_lazy as _

# Define user types
class UserType(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name

# User Custom Model
class CustomUser(AbstractUser):
    user_type = models.CharField(max_length=20, choices=[
        ('visitor', 'Visitor'),
        ('traverser', 'Traverser'),
        ('administrator', 'Administrator')
    ], default='visitor')

    # Adding related_name to avoid clashes
    groups = models.ManyToManyField(
        Group,
        verbose_name=_('groups'),
        blank=True,
        help_text=_('The groups this user belongs to.'),
        related_name='customuser_set',
        related_query_name='customuser',
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=_('user permissions'),
        blank=True,
        help_text=_('Specific permissions for this user.'),
        related_name='customuser_set',
        related_query_name='customuser',
    )

    def __str__(self):
        return self.username
        