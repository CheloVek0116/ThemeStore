from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.views.generic import View, ListView, DetailView, FormView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login

from cart.cart import Cart
from .models import *
from .forms import *
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


class SignUpView(CreateView):
    """Вьюха регистрации пользователя"""
    form_class = SignUpForm
    success_url = ''
    template_name = 'registration/signup.html'

    def form_valid(self, form):
        # Создаём пользователя, если данные в форму были введены корректно.
        form.save()
        self.success_url = reverse('profileUser:LoginRedirect', kwargs={'login_user': form.cleaned_data['username'], 'password': form.cleaned_data['password1']})
        # Вызываем метод базового класса
        return super(SignUpView, self).form_valid(form)

def LoginRedirect(request, login_user, password):
    user = User.objects.get(username=authenticate(request, username=login_user, password=password))
    login(request, user)
    return redirect(user.get_absolute_url())