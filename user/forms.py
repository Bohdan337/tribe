from django import forms
from .models import CustomUser
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.forms.widgets import Input, PasswordInput, EmailInput
from django_recaptcha.fields import ReCaptchaField
from django_recaptcha.widgets import ReCaptchaV2Checkbox




class CustomUserCreationForm(UserCreationForm, forms.Form):
    name = forms.CharField(max_length=255, widget=Input(attrs={'class': 'm-3 h-12 rounded-lg p-2 bg-gray-900 text-white', 'placeholder': 'Name'}))
    surname = forms.CharField(max_length=255, widget=Input(attrs={'class': 'm-3 h-12 rounded-lg p-2 bg-gray-900 text-white', 'placeholder': 'Surname'}))
    email = forms.CharField(max_length=255, widget=EmailInput(attrs={'class': 'm-3 h-12 rounded-lg p-2 bg-gray-900 text-white', 'placeholder': 'Email'}))
    password1 = forms.CharField(max_length=255, widget=PasswordInput(attrs={'class': 'm-3 h-12 rounded-lg p-2 bg-gray-900 text-white', 'placeholder': 'Password'}))
    password2 = forms.CharField(max_length=255, widget=PasswordInput(attrs={'class': 'm-3 h-12 rounded-lg p-2 bg-gray-900 text-white', 'placeholder': 'Check password'}))
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox())

    class Meta:
        model = CustomUser
        fields = ('name', 'surname', 'email', 'captcha')



class CustomLoginForm(AuthenticationForm):
    username = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'm-3 h-12 rounded-lg p-2 bg-gray-900 text-white', 'placeholder': 'Email'}), label='Email')    
    password = forms.CharField(max_length=255, widget=PasswordInput(attrs={'class': 'm-3 h-12 rounded-lg p-2 bg-gray-900 text-white', 'placeholder': 'Password'}))
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox())


class ChangeImageForm(forms.Form):
    image = forms.ImageField()


class UserSearchForm(forms.Form):
    email = forms.CharField(max_length=255, widget=Input(attrs={'class': 'm-2 h-36 rounded-lg p-2 bg-gray-900 text-white', 'placeholder' : 'user email..'}))


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['email', 'name', 'surname', 'is_student', 'is_teacher']
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'm-2 h-36 rounded-lg p-2 bg-blue-950 text-white', 'placeholder': 'user email..'}),
            'name': forms.TextInput(attrs={'class': 'm-2 h-36 rounded-lg p-2 bg-blue-950 text-white', 'placeholder': "user's name.."}),
            'surname': forms.TextInput(attrs={'class': 'm-2 h-36 rounded-lg p-2 bg-blue-950 text-white', 'placeholder': "user's surname.."}),
        }