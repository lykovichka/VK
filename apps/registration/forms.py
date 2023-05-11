from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class UserRegisterForm(UserCreationForm):
    username = forms.CharField(label='Логин', required=True)
    first_name = forms.CharField(label='Имя', required=True)
    last_name = forms.CharField(label='Фамилия', required=True)
    email = forms.EmailField(required=True)

    error_messages = {
        'duplicate_username': "Пользователь с таким именем уже существует",
        'password_mismatch': "Введенные пароли не совпадают",
    }

    field_order = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super(UserRegisterForm, self).__init__(*args, **kwargs)
        self.fields = ['username', 'email', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise ValueError('Email Already Exists')
        return email
