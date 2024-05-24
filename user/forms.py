from django import forms
from .models import CustomUser
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.forms.widgets import Input, PasswordInput
from django_recaptcha.fields import ReCaptchaField
from django_recaptcha.widgets import ReCaptchaV2Checkbox




class CustomUserCreationForm(UserCreationForm, forms.Form):
    name = forms.CharField(max_length=255, widget=Input(attrs={'class': 'm-3 h-12 rounded-lg p-2 bg-gray-900 text-white', 'placeholder': 'Name'}))
    surname = forms.CharField(max_length=255, widget=Input(attrs={'class': 'm-3 h-12 rounded-lg p-2 bg-gray-900 text-white', 'placeholder': 'Surname'}))
    email = forms.CharField(max_length=255, widget=Input(attrs={'class': 'm-3 h-12 rounded-lg p-2 bg-gray-900 text-white', 'placeholder': 'Email'}))
    password1 = forms.CharField(max_length=255, widget=PasswordInput(attrs={'class': 'm-3 h-12 rounded-lg p-2 bg-gray-900 text-white', 'placeholder': 'Password'}))
    password2 = forms.CharField(max_length=255, widget=PasswordInput(attrs={'class': 'm-3 h-12 rounded-lg p-2 bg-gray-900 text-white', 'placeholder': 'Check password'}))
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox())

    class Meta:
        model = CustomUser
        fields = ('name', 'surname', 'email')



class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(widget=Input(attrs={'class': 'm-3 h-12 rounded-lg p-2 bg-gray-900 text-white', 'placeholder': 'Name und surname'}))
    password = forms.CharField(widget=PasswordInput(attrs={'class': 'm-3 h-12 rounded-lg p-2 bg-gray-900 text-white', 'placeholder': 'Password'}))
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox())
