from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import View, ListView, DetailView, FormView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.files.base import ContentFile

from .models import *
from .forms import *


class ProductList(ListView):
	
	def get(self, request, **kwargs):
		category = kwargs.get('category')
		if category:
			category = Category.objects.get(name=category)
			products = Product.objects.filter(categories=category)
		else: 
			products = Product.objects.all()

		products = products.order_by('-ratings__average')

		context = {
				'products': products,
				}
		return render(request, 'product/list.html', context=context)
  


class ProductDetail(DetailView):

	def get(self, request, username, slug):
		product = get_object_or_404(Product, author__username=username, slug=slug)
		images = ProductImage.objects.filter(product=product)
		
		context = {
				'product': product,
				'images': images,
				}
		return render(request, 'product/detail.html', context=context) 


class ProductAdd(LoginRequiredMixin, FormView):

	def get(self, request, **kwargs):
		form = ProductForm()
		return render(request, 'product/create.html', context={'form': form})

	def post(self, request, **kwargs):
		form = ProductForm(request.POST, request.FILES)
		print(request.FILES)
		if form.is_valid():
			print(213)
			product = Product.objects.create(
											author=request.user,
											name=form.cleaned_data['name'],
											slug=form.cleaned_data['slug'],
											description=form.cleaned_data['description'],
											price=form.cleaned_data['price']
											)
			for f in request.FILES.getlist('images'):
				data = f.read() #Если файл целиком умещается в памяти
				photo = ProductImage(product=product)
				photo.image.save(f.name, ContentFile(data))
				photo.save()
				return redirect(product)
		return render(request, 'product/create.html', context={'form': form})
