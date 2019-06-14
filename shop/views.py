from django.shortcuts import render, get_object_or_404
from .models import *
from django.views.generic import View, ListView, DetailView, FormView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin


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
