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

@notAutheticated #checks the authentication, if authenticated then redirect
def register(request):

    reg_form = Registration()
    if request.method == 'POST':
        reg_form = Registration(request.POST)
        if reg_form.is_valid():
            user = reg_form.save()
            username = reg_form.cleaned_data.get('username')
            group = Group.objects.get(name='customers')
            user.groups.add(group)
            messages.success(request, 'account ' + username + ' created')
            time.sleep(1)
            return redirect('login')

    ctx = {'form':reg_form}
    return render(request, 'users/register.html', ctx)


@notAutheticated #checks the authentication, if authenticated then redirect
def Login(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            time.sleep(1)
            return redirect('home')
        else:
            messages.info(request, 'username or password incorrect')


    ctx = {}
    return render(request, 'users/login.html', ctx)

def Logout(request):
    logout(request)
    time.sleep(1)
    return redirect('home')


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def admin(request):

    users= get_user_model().objects.all()
    groups = Group.objects.all()
    ctx = {'users':users, 'groups':groups}
    return render(request, 'users/admin.html', ctx)

@login_required(login_url='login')
@allowed_users(allowed_roles=['staff', 'admin'])
def moderation(request):

    users= get_user_model().objects.all()
    
    ctx = {'users':users}
    return render(request, 'users/moderator.html', ctx)


def update_usr(request, usr_id):
    usr = User.objects.get(id=usr_id)
    form = usr_dashboardUpdate(instance=usr)

    if request.method == 'POST':
        form = usr_dashboardUpdate(request.POST, instance=usr)
        if form.is_valid():
            form.save()
            current = request.user
            if current.is_superuser:
                return redirect('/usr/admin')
            else:
                return redirect('/usr/moderation')

    ctx = {'form':form}
    return render(request, 'users/update_usr.html', ctx)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def delete_usr(request, usr_id):
    user = User.objects.get(id=usr_id)

    if request.method == 'POST':
        user.delete()
        current = request.user
            if current.is_superuser:
                return redirect('/usr/admin')
            else:
                return redirect('/usr/moderation')

    ctx = {'user':user}
    return render(request, 'users/usr_delete.html', ctx)