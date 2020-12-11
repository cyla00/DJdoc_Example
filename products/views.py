from django.shortcuts import render, redirect
from django.http import HttpResponse
import time
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
# Create your views here.
from .forms import *
from .decorators import *

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def add_product(request):
    add_form = product_form()
    if request.method == 'POST':
        add_form = product_form(request.POST)
        if add_form.is_valid():
            add_form.save()
            return redirect('product_list')

    ctx = {'form':add_form}
    return render(request, 'products/add_product.html', ctx)

def products(request):
    list = Product.objects.all()
    ctx = {'list':list}
    return render(request, 'products/product_list.html', ctx)

def show_product(request, p_id):
    single = Product.objects.filter(id=p_id)
    ctx = {'single':single}
    return render(request, 'products/show_product.html', ctx)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def update_prod(request, pr_id):

    prod = Product.objects.get(id=pr_id)
    form = product_form(instance=prod)

    if request.method == 'POST':
        form = product_form(request.POST, instance=prod)
        if form.is_valid():
            form.save()
            return redirect('product_list')

    ctx = {'form':form}
    return render(request, 'products/modify_product.html', ctx)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def delete_prod(request, pr_id):
    prod = Product.objects.get(id=pr_id)

    if request.method == 'POST':
        prod.delete()
        return redirect('product_list')

    ctx = {'prod':prod}
    return render(request, 'products/delete.html', ctx)