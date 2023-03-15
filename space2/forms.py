from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

User = get_user_model()

class RegistrationForm(forms.ModelForm):
    
    class Meta:
        model = User
        fields = ['full_name', 'email', 'password', 'confirm_password']
        