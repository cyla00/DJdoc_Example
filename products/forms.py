from django.forms import ModelForm
from .models import *
from django import forms

class product_form(ModelForm):
    class Meta:
        model = Product
        fields = '__all__'