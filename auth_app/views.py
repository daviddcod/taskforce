
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .forms import RegistrationForm, LoginForm
from .models import CustomUser
from django.views.decorators.csrf import ensure_csrf_cookie


@ensure_csrf_cookie
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Optionally log the user in immediately

            # Redirect to the 'select_plan' view in the 'plan_selection' app
            return redirect('plan_selection:list_plans')
    else:
        form = RegistrationForm()

    return render(request, 'register.html', {'form': form})

@ensure_csrf_cookie
def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                # Use reverse to get the URL for 'home.html'
                home_url = reverse('home')  # 'home' should be the name of your URL pattern
                return redirect(home_url)
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('home')

@login_required(login_url='register')
def home(request):
    return render(request, 'home.html')

def dashboard(request):
    return render(request, 'dashboard.html')
        
