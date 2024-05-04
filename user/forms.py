from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django import forms

class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs) -> None:
        super(LoginForm, self).__init__(*args, **kwargs)


class SignupForm(UserCreationForm):
    email = forms.EmailField(label='Email', widget=forms.EmailInput(), required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']