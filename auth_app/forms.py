
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class RegistrationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'password1', 'password2', 'user_type']

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password', 'user_type')  # Only show these fields initially
        help_texts = {
            'username': 'A unique username for your profile.',
            'email': 'We\'ll never share your email with anyone else.',
            # Add more help texts for other fields as needed
        }
    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            # Set default values for the extra fields
            CustomUser.objects.create(
                user=user,
                level=1,  # Default level
                experience=0,  # Default experience
                prestige=1,  # Default prestige
                health=200,  # Default health
                endurance=100,  # Default endurance
                mind=75,  # Default mind
            )
        return user


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
            