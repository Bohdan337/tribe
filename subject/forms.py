from django import forms
from .models import Subject


class CourseForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ['title', 'summary']



class AddStudentForm(forms.Form):
    email = forms.EmailField(label='Email студента', max_length=254)

