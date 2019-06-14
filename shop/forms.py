from django import forms
from .models import *


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('name', 'slug', 'description', 'categories', 'price',)


class ProductImageForm(forms.ModelForm):
    class Meta:
        model = ProductImage
        fields = ('product', 'preview', 'image',)