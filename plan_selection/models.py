from django.db import models
from django.contrib.auth.models import Group

class Plan(models.Model):
    PLAN_CHOICES = [
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
        ('yearly', 'Yearly'),
    ]

    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    billing_cycle = models.CharField(max_length=10, choices=PLAN_CHOICES)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, null=True)  # Temporarily allow null

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.group:  # If this is a new object or has no group set
            # Set default group as 'Traverser' (or any other logic you prefer)
            default_group, _ = Group.objects.get_or_create(name='Traverser')
            self.group = default_group
        super(Plan, self).save(*args, **kwargs)
