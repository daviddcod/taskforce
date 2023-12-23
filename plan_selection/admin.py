# admin.py of your application

from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from .models import Plan

class PlanAdminForm(forms.ModelForm):
    class Meta:
        model = Plan
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(PlanAdminForm, self).__init__(*args, **kwargs)
        # Limit choices for the group field to 'Visitor', 'Traverser', and 'Administrator'
        self.fields['group'].queryset = Group.objects.filter(name__in=['Visitor', 'Traverser', 'Administrator'])

class PlanAdmin(admin.ModelAdmin):
    form = PlanAdminForm

admin.site.register(Plan, PlanAdmin)
