from django.shortcuts import render
from .models import *

# Create your views here.
def products(request):
    list = Product.objects.all()
    ctx = {'list':list}
    return render(request, 'products/product_list.html', ctx)

def show_product(request, p_id):
    single = Product.objects.filter(id=p_id)
    ctx = {'single':single}
    return render(request, 'products/show_product.html', ctx)