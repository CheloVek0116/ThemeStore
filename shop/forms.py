from django import forms
from django.forms import formset_factory

from .models import *


class ProductForm(forms.Form):
	name        = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
	description = forms.CharField(widget=forms.Textarea(attrs={'class':'form-control', 'rows': '4'}))
	categories  = forms.MultipleChoiceField(choices=(('wordpress', 'WordPress'),
													 ('html', 'HTML'),
													 ('cms', 'CMS'),
													 ('ui', 'UI Дизайн'),
													 ('scripts', 'Скрипты')),
											required=False,
											widget=forms.CheckboxSelectMultiple())

	price       = forms.DecimalField(max_digits=10, decimal_places=2, widget=forms.NumberInput(attrs={'class':'form-control'}))
	file        = forms.FileField(widget=forms.FileInput(attrs={'accept':'application/zip'}))


class ImagesForm(forms.Form):
	images      = forms.ImageField(label='Фотографии', widget=forms.FileInput(attrs={'onchange':'readURL(this);', 'style': 'display: none;'}))
	preview     = forms.BooleanField(label='', required=False, widget=forms.CheckboxInput(attrs={'disabled':'', 'onchange':'checked_preview(this);'}))

ImagesFormSet = formset_factory(ImagesForm, extra=5, max_num=5, min_num=1, validate_min=True, validate_max=True)
