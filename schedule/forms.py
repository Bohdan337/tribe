from django import forms
from .models import Schedule
from django.forms.widgets import Input, TimeInput, URLInput
from user.models import CustomUser


class ScheduleForm(forms.ModelForm):
    title = forms.CharField(max_length=255, widget=Input(attrs={'class': 'h-12 rounded-lg p-2 bg-gray-900 text-white', 'placeholder': 'Title'}))
    summary = forms.CharField(max_length=1024, widget=Input(attrs={'class': 'h-12 rounded-lg p-2 bg-gray-900 text-white', 'placeholder': 'Description'}))
    duration = forms.TimeField(widget=TimeInput(attrs={'class': 'h-12 rounded-lg p-2 bg-gray-900 text-white', 'placeholder': 'Duration'}))
    link = forms.URLField(widget=URLInput(attrs={'class': 'h-12 rounded-lg p-2 bg-gray-900 text-white', 'placeholder': 'URL'}))

    class Meta:
        model = Schedule
        fields = ['duration', 'link', 'title', 'summary']