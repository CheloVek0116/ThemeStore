from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import View, ListView, DetailView, FormView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin

from cart.cart import Cart
from .models import *
from shop.models import *


class ProfileDetail(ListView):
	
	def get(self, request, **kwargs):
		username = kwargs.get('username')
		profile = get_object_or_404(User, username=username)
		context = {
				'profile': profile
		}
		return render(request, 'profile/profile.html', context=context)

class ProfileCards(ListView):
	
	def get(self, request, **kwargs):
		username = kwargs.get('username')
		profile = get_object_or_404(User, username=username)
		products = Product.objects.filter(author=profile)
		context = {
				'products': products,
				'profile' : profile
		}
		return render(request, 'profile/profile_cards.html', context=context)