# WINDOWS
## requirements:
* install => [PostgreSQL](https://www.enterprisedb.com/downloads/postgres-postgresql-downloads)<br/>
* install => [Anaconda or Miniconda](https://www.anaconda.com/products/individual)

## 1) setup of Anaconda virtual env for django
* to create a new virtual envyronment: ```$ conda create --name ENV_NAME```<br/>
* to activate the environment: ```$ conda activate ENV_NAME```<br/>
=>[useful docs for environment management](https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html#creating-an-environment-with-commands)<=<br/>

#### -now you are ready to install all the packages you need in the environment to run your projects

[install django](https://anaconda.org/anaconda/django):<br/>
```$ conda install -c anaconda django```<br/>
-to choose the django and/or python version to install:<br/>
```$ conda install -c anaconda django=VERSION_HERE python=VERSION_HERE```<br/>
latest stable release it's fine.

[psycopg2](https://anaconda.org/anaconda/psycopg2):<br/>
```$ conda install -c anaconda psycopg2```<br/>

[install PostgreSQL](https://anaconda.org/anaconda/postgresql):<br/>
```$ conda install -c anaconda postgresql```<br/>

optional => [debug toolBar](https://anaconda.org/conda-forge/django-debug-toolbar):<br/>
```$ conda install -c conda-forge django-debug-toolbar```<br/>
as of now it works only with django 2.2 because of compatibility issues with the "six" package.

## 2) creation and connection of a django project
in the command line climb the path you want to put your project in and run ```$ django-admin startproject PROJECT_NAME```, a new folder named PROJECT_NAME and a ```./manage.py``` file are created.<br/>
Inside the folder there is a ```./settings.py``` file with a ```DATABASES``` variable, modify it depending on your [database type](https://docs.djangoproject.com/en/3.1/ref/settings/#databases).
* for postgress replace it with:
```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'DB_NAME',
        'USER': 'DB_USER',
        'PASSWORD': 'DB_PASWD',
        'HOST': 'localhost',    #if testing locally use localhost, if in a server use server host
        'PORT': '5432', #default local port, if in a server specify the port
    }
}
```

### -run the script
to run the script from the anaconda terminal with your django env activated climb to root path of your project folder where ```./manage.py``` is located and run  ```$ python manage.py runserver```.
*in the logs you will see a migration request, thats because django by default creates some default tables such as Users, Groups where for example your default admin user will be located.
if you wish to extend one of those tables or modify them dont run the migration yet, if the default database tables are suited for you just run ```$ python manage.py migrate```.

* check log => ```Starting development server at http://127.0.0.1:8000/``` (if running in local), open the url on a browser and if all was setup correctly a django welcome page should show.

## 3) start writing the project
* The django file structure is basically a file "project" that contains "apps", project urls.py is responsible for the url routing in your site from pages to apps<br/>
![file structure](https://djangobook.com/wp-content/uploads/structure_drawing1_new.png "base django project structure")

* create an app with: ```$ django manage.py startapp NAME_APP```<br/>
to add the app at the main project, go to root path ./settings.py and under INSTALLED_APPS, add as an app the folder name of the app just created.

## 4) app manipulation
the app itself is devided in different parts:
* urls.py is responsible for the internal url routing of the app (example: "home" will be "/home") and when we search /home in the url, the view linked to that will be executed, example:
```py
from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home, name='home'),
    path('products/', views.products, name='products'),
]


#to pass a variable into the url (to get the ID of a specific element: "ctx_id")
path('products/<str:ctx_id>/', views.products, name='home')
#the home/ url will require the id to be filled, example: home/1/
```
* views.py is responsible of the rendering of your html files and the database interactions (queries etc..), example:
```py
#just a home page, it renders the templates/NAME_APP/home.html
def home(request):
    ctx = {}
    return render(request, 'NAME_APP/home.html', ctx)


def products(request):
    products = product.objects.all()
    ctx = {'products':products}  
    #what the ctx variable  does is making a variable that we can recall inside an html file using tags, example:  <p>{{products}}</p> . we can also use IF and FOR inside {%  %} 
    return render(request, 'NAME_APP/products.html', ctx)
```
* models.py is responsible of the table structure of your database, every object in that file is a table that will be shown into the database every time we migrate it, example:
```py
from django.db import models
# Create your models here.
class product(models.Model):
    title = models.CharField(max_length=200, null=True)
    description = models.TextField(max_length=200, null=True)
    price = models.DecimalField(decimal_places=2, max_digits=20, null=True)
    summary = models.TextField(default='null', null=True)
```
to push that into the database we have to prepare the actions we want to execute running ```$ python manage.py makemigrations``` this will automatically create a migration file with a denomination like "0001" "0002" etc...
then we make the actual migration with ```$ python manage.py migrate``` and at this point the database is up to date.
If we create a new column while having data in that table, the column will be filled with the "null" value if ```null=True``` is set for all the rows of that table,
if we choose to modify the type of an already existent column for example from textField to Decimal, the migration will throw an error such as ```django.db.utils.DataError: invalid input syntax for type numeric:```,
trying to eliminate a filled column, the site will nor recognise the column anymore, but looking at the database table the column will still be present and filled.
To grant more flexibility, django has it's shell that behaves like a psql shell, so running this command ```$ python manage.py dbshell``` will give us the possibility to manipulate the DB from terminal and so the possibility to DROP unwanted columns.

* forms.py manages our custom forms, if we want to create a from for the product table, we would recall that object and select the elements we want to include inside the form, example:
```py
from django import forms
from django.forms import ModelForm
from .models import *

class product_from(ModelForm):
    class Meta:
        model = product  #here we recall the product object inside models.py
        fields = ['title', 'price'] #the form will be only composed by the title and the price of that obejct
        fields = '__all__' #this will catch all the fields inside the table automatically.
```
* filters.py manages a "filtration form" like a custom searchbar for our DB tables, example:
```py
import django_filters
from django_filters import CharFilter
from .models import *

class productFilter(django_filters.FilterSet):
    name = CharFilter(field_name='title', lookup_expr='icontains')
    category = CharFilter(field_name='description', lookup_expr='icontains')
    class Meta:
        model = product
        fields = ['title', 'description']

# checks if the user input is contained in the title or the description in any product row
```
* decorators.py are normally used to setup limitations to your views functions so only the roles you select are able to access that view or that url (website page), example:
```py
from django.http import HttpResponse
from django.shortcuts import redirect
import time

#this function will check if the viewer/user is an authenticated one or not, if your site needs a login system, it will check if the user is logged in (useful if a page is shown only to logged in users)
def notAutheticated(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        else:
            return view_func(request, *args, **kwargs)

    return wrapper_func


# this function will make a query asking for the groups we have in our database/users groups, good practice is to create groups with some determined roles so every user part of that group will have the specific permissions already setup.
def allowed_users(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            group = None
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name #gets all the group name of the user

            if group in allowed_roles:
                return view_func(request, *args, **kwargs)
            else:
                time.sleep(1)
                return redirect('home') #if the user doesnt have the permission, it will be redirected to the gome page
        return wrapper_func
    return decorator
```
# versions used:
* python 3.8.5
* django 3.1.2
* postgresql 12.2
* psycopg2 2.8.5

# useful links docs and tutorials:
* [official django docs](https://www.djangoproject.com/)
* a very well done [tutorial](https://www.youtube.com/watch?v=xv_bwpA_aEA&list=PL-51WBLyFTg2vW-_6XBoUpE7vpmoR3ztO) with a series of videos showing a django project creation
