from django.shortcuts import render

# Create your views here.

from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .forms import RegistrationForm, LoginForm

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = RegistrationForm()
    return render(request, 'auth_app/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return redirect('auth_app_home')
    else:
        form = LoginForm()
    return render(request, 'auth_app/login.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('auth_app_logout')

@login_required(login_url='register')
def home(request):
    return render(request, 'auth_app/home.html')

def dashboard(request):
    return render(request, 'dashboard.html')
        