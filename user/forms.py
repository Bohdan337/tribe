from django import forms
from .models import CustomUser
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, SetPasswordForm
from django.forms.widgets import Input, PasswordInput, EmailInput
from django_recaptcha.fields import ReCaptchaField
from django_recaptcha.widgets import ReCaptchaV2Checkbox




# This class `CustomUserCreationForm` extends `UserCreationForm` and `forms.Form`, adding custom
# fields for name, surname, email, passwords, and a ReCaptcha field for user registration.
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



# The `CustomLoginForm` class extends `AuthenticationForm` and includes fields for username (email),
# password, and a ReCaptcha field.
class CustomLoginForm(AuthenticationForm):
    username = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'm-3 h-12 rounded-lg p-2 bg-gray-900 text-white', 'placeholder': 'Email'}), label='Email')    
    password = forms.CharField(max_length=255, widget=PasswordInput(attrs={'class': 'm-3 h-12 rounded-lg p-2 bg-gray-900 text-white', 'placeholder': 'Password'}))
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox())



# The `UpdatePasswordForm` class extends `SetPasswordForm` and includes a ReCaptcha field for updating
# a user's password.
class UpdatePasswordForm(SetPasswordForm):
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox())
    class Meta:
        model=CustomUser
        fields= ['new_password1', 'new_password2']



# The `ChangeImageForm` class in Python defines a form with a single field for uploading an image.
class ChangeImageForm(forms.Form):
    image = forms.ImageField()



# The class `UserSearchForm` defines a form with a field for user email input, styled with specific
# CSS classes and placeholder text.
class UserSearchForm(forms.Form):
    email = forms.CharField(max_length=255, widget=Input(attrs={'class': 'm-2 h-36 rounded-lg p-2 bg-gray-900 text-white', 'placeholder' : 'user email..'}))


# The `UserUpdateForm` class defines a form for updating user information with specified fields and
# widgets for styling.
class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['email', 'name', 'surname', 'is_student', 'is_teacher']
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'm-2 h-36 rounded-lg p-2 bg-blue-950 text-white', 'placeholder': 'user email..'}),
            'name': forms.TextInput(attrs={'class': 'm-2 h-36 rounded-lg p-2 bg-blue-950 text-white', 'placeholder': "user's name.."}),
            'surname': forms.TextInput(attrs={'class': 'm-2 h-36 rounded-lg p-2 bg-blue-950 text-white', 'placeholder': "user's surname.."}),
        }