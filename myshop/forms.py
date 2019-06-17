from django.contrib.auth import get_user_model

 # импорты встроенной регистрации
from django.contrib.auth.forms import UserCreationForm

USER = get_user_model()

class SignUpForm(UserCreationForm):
    """Форма регистрации пользователя"""
    class Meta:
        model = USER
        fields = ('username', "email", 'password1', 'password2')
