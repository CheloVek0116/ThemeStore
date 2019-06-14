from django import forms
from django.db import models
from .models import *


class ProductForm(forms.Form):
	name        = forms.CharField(label="Название")
	slug        = forms.SlugField()
	description = forms.CharField(label="Описание")
	price       = forms.DecimalField(max_digits=10, decimal_places=2, label="Цена")
	images      = forms.ImageField(label='Фотографии', widget=forms.FileInput(attrs={'multiple': 'multiple'}))