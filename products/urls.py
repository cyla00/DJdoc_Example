from django.urls import path
from . import views

urlpatterns = [
    path('list/', views.products, name='product_list'),
    path('more/<str:p_id>/', views.show_product, name='show_product'),
]