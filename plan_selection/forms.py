# plan_selection/forms.py

from django import forms
from .models import Plan

class PlanForm(forms.ModelForm):
    class Meta:
        model = Plan
        fields = ['name', 'description', 'price', 'billing_cycle', 'group']  # include 'group'
