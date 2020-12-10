from django.urls import path
from . import views
from .views import *

urlpatterns = [
    path('list/', views.products, name='product_list'),
    path('more/<str:p_id>/', views.show_product, name='show_product'),
    path('add/', views.add_product, name='add_product'),
    path('modify/<str:pr_id>/', views.update_prod, name='update_prod'),
]