from django.shortcuts import render
from django.views.generic import CreateView
from django.contrib.auth.forms import UserCreationForm
from .forms import *
# Create your views here.

def present_page(request):
    return render(request, "Present.html")

class SignUpForm(CreateView):
    """Вьюха регистрации пользователя"""
    form_class = SignUpForm
    success_url = ''
    template_name = 'registration/signup.html'

    def form_valid(self, form):
        # Создаём пользователя, если данные в форму были введены корректно.
        form.save()

        # Вызываем метод базового класса
        return super(SignUpForm, self).form_valid(form)