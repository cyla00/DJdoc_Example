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



############################# moderation and user management #############################


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
    settings = Setting.objects.all()
    ctx = {'users':users, 'groups':groups, 'settings':settings}
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
            current_user = request.user
            if current_user.is_superuser:
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
        return redirect('/usr/admin')

    ctx = {'user':user}
    return render(request, 'users/delete.html', ctx)



############################# SETTINGS #############################
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def add_settings(request):
    add_form = settings_form()
    if request.method == 'POST':
        add_form = settings_form(request.POST)
        if add_form.is_valid():
            add_form.save()
            return redirect('admin')

    ctx = {'form':add_form}
    return render(request, 'users/setting_add.html', ctx)



@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def update_settings(request, sett_id):
    settings = Setting.objects.get(id=sett_id)
    form = settings_form(instance=settings)

    if request.method == 'POST':
        form = settings_form(request.POST, instance=settings)
        if form.is_valid():
            form.save()
            current_user = request.user
            if current_user.is_superuser:
                return redirect('/usr/admin')
            else:
                return redirect('/usr/moderation')

    ctx = {'form':form}
    return render(request, 'users/setting_update.html', ctx)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def delete_setting(request, sett_id):
    settings = Setting.objects.get(id=sett_id)

    if request.method == 'POST':
        settings.delete()
        return redirect('/usr/admin')

    ctx = {'settings':settings}
    return render(request, 'users/delete.html', ctx)



############################# Groups #############################
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def add_group(request):
    add_form = goroup_form()
    if request.method == 'POST':
        add_form = goroup_form(request.POST)
        if add_form.is_valid():
            add_form.save()
            return redirect('admin')

    ctx = {'form':add_form}
    return render(request, 'users/group_add.html', ctx)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def update_group(request, group_id):
    group = Group.objects.get(id=group_id)
    form = goroup_form(instance=group)

    if request.method == 'POST':
        form = goroup_form(request.POST, instance=group)
        if form.is_valid():
            form.save()
            current_user = request.user
            if current_user.is_superuser:
                return redirect('/usr/admin')
            else:
                return redirect('/usr/moderation')

    ctx = {'form':form}
    return render(request, 'users/group_update.html', ctx)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def delete_group(request, group_id):
    group = Group.objects.get(id=group_id)

    if request.method == 'POST':
        group.delete()
        return redirect('/usr/admin')

    ctx = {'group':group}
    return render(request, 'users/delete.html', ctx)