from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
import time
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group

# Create your views here.
from .forms import *
from .decorators import *


def home(request):

    ctx = {}
    return render(request, 'main/home.html', ctx)

def about(request):
    ctx = {}
    return render(request, 'main/about.html', ctx)