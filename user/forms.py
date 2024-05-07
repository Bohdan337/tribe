from django import forms
from .models import CustomUser, Student, Teacher, ChiefTeacher
from django.contrib.auth.forms import UserCreationForm



class CustomUserCreationForm(UserCreationForm):
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