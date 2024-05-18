from django import forms
from .models import CustomUser
from django.contrib.auth.forms import UserCreationForm
from django.forms.widgets import Input, PasswordInput, EmailInput



class CustomUserCreationForm(UserCreationForm, forms.Form):
    name = forms.CharField(max_length=255, widget=Input(attrs={'class': 'm-3 h-12 rounded-lg p-2 bg-gray-900 text-white', 'placeholder': 'Name'}))
    surname = forms.CharField(max_length=255, widget=Input(attrs={'class': 'm-3 h-12 rounded-lg p-2 bg-gray-900 text-white', 'placeholder': 'Surname'}))
    email = forms.CharField(max_length=255, widget=EmailInput(attrs={'class': 'm-3 h-12 rounded-lg p-2 bg-gray-900 text-white', 'placeholder': 'Email'}))
    password1 = forms.CharField(max_length=255, widget=PasswordInput(attrs={'class': 'm-3 h-12 rounded-lg p-2 bg-gray-900 text-white', 'placeholder': 'Password'}))
    password2 = forms.CharField(max_length=255, widget=PasswordInput(attrs={'class': 'm-3 h-12 rounded-lg p-2 bg-gray-900 text-white', 'placeholder': 'Check password'}))

    class Meta:
        model = CustomUser
        fields = ('name', 'surname', 'email')

