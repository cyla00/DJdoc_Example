from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    
    #apps
    path('products/', include('products.urls'), name='products'),
    path('usr/', include('users.urls'), name='users'),
]