
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .forms import RegistrationForm, LoginForm
from .models import CustomUser
from django.views.decorators.csrf import ensure_csrf_cookie


from django.contrib.auth import login
from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm  # Make sure to import the correct form
from django.views.decorators.csrf import ensure_csrf_cookie

@ensure_csrf_cookie  # Keep this decorator if you need CSRF token set for AJAX requests
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)  # Use the new CustomUserCreationForm
        if form.is_valid():
            user = form.save()  # This will also create UserProfile with default values
            login(request, user)  # Optionally log the user in immediately

            # Choose the appropriate redirect based on your application's flow
            return redirect('home_app:welcome')  # Adjust the redirect as needed
    else:
        form = CustomUserCreationForm()  # Use the new CustomUserCreationForm

    # Adjust the path to your registration template as needed
    return render(request, 'wdmmorpg/register.html', {'form': form})


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
                # Use reverse to get the URL for 'user_home.html'
                return redirect('home_app:welcome')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('home_app:welcome')

@login_required()
def home(request):
    return render(request, 'home.html')

def dashboard(request):
    return render(request, 'dashboard.html')
        
