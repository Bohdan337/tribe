from django import forms
from .models import Subject


class CourseForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ['title', 'summary']

