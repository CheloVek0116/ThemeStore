 # импорты встроенной регистрации
from django.contrib.auth.forms import UserCreationForm
from .models import User


class SignUpForm(UserCreationForm):
    """Форма регистрации пользователя"""
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'password1', 'password2')
