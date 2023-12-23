# plan_selection/views.py

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Plan

# plan_selection/views.py

def list_plans(request):
    plans = Plan.objects.all()
    return render(request, 'list_plans.html', {'plans': plans})

# plan_selection/views.py

from django.shortcuts import render, redirect
from .forms import PlanForm

@login_required
def select_plan(request):
    if request.method == 'POST':
        form = PlanForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('payment_proccesor:complete')  # Redirect to a success page
    else:
        form = PlanForm()  # An unbound form

    return render(request, 'plan_selection.html', {'form': form})

def list_plans(request):
    plans = Plan.objects.all()  # Retrieve all plans from the database
    return render(request, 'list_plans.html', {'plans': plans})

