from django import forms
from .models import Subject
from django.forms.widgets import Input


class CourseForm(forms.ModelForm, forms.Form):
    title = forms.CharField(max_length=255, widget=Input(attrs={'class': 'm-3 h-12 rounded-lg p-2 bg-gray-900 text-white', 'placeholder': 'Title'}))
    summary = forms.CharField(max_length=1024, widget=Input(attrs={'class': 'm-3 h-12 rounded-lg p-2 bg-gray-900 text-white', 'placeholder': 'Description'}))

    class Meta:
        model = Subject
        fields = ['title', 'summary']

