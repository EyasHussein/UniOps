from django import forms
from django.contrib.auth.forms import UserCreationForm #^ this will hash the password 
from .models import User

class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'role', 'department')
