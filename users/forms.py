from django.forms import ModelForm
from .models import *
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import authenticate, login, logout, get_user_model
from django import forms
from django.contrib.auth.models import User, Group, Permission

class Registration(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class usr_dashboardUpdate(UserChangeForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'groups', 'first_name', 'last_name', 'is_staff']
        # fields = '__all__'