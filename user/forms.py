from django import forms
from .models import CustomUser, Student, Teacher, ChiefTeacher
from django.contrib.auth.forms import UserCreationForm
from django.forms.widgets import Input, PasswordInput



class CustomUserCreationForm(UserCreationForm, forms.Form):
    name = forms.CharField(max_length=255, widget=Input(attrs={'class': 'm-3 h-12 rounded-lg p-2 bg-gray-900 text-white', 'placeholder': 'Name'}))
    surname = forms.CharField(max_length=255, widget=Input(attrs={'class': 'm-3 h-12 rounded-lg p-2 bg-gray-900 text-white', 'placeholder': 'Surname'}))
    email = forms.CharField(max_length=255, widget=Input(attrs={'class': 'm-3 h-12 rounded-lg p-2 bg-gray-900 text-white', 'placeholder': 'Email'}))
    password = forms.CharField(max_length=255, widget=PasswordInput(attrs={'class': 'm-3 h-12 rounded-lg p-2 bg-gray-900 text-white', 'placeholder': 'Password'}))
    password2 = forms.CharField(max_length=255, widget=PasswordInput(attrs={'class': 'm-3 h-12 rounded-lg p-2 bg-gray-900 text-white', 'placeholder': 'Check password'}))

    class Meta:
        model = CustomUser
        fields = ('username', 'email')

class StudentForm(forms.ModelForm):
    email = forms.EmailField(max_length=255)

    class Meta:
        model = Student
        fields = ('name', 'surname', 'email')

class TeacherForm(forms.ModelForm):
    email = forms.EmailField(max_length=255)

    class Meta:
        model = Teacher
        fields = ('name', 'surname', 'email')

class ChiefTeacherForm(forms.ModelForm):
    class Meta:
        model = ChiefTeacher
        fields = ('name', 'surname', 'email')