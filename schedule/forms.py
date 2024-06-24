from django import forms
from .models import Schedule
from django.forms.widgets import Input, TimeInput, URLInput, DateTimeInput, TextInput, DateInput
from user.models import CustomUser


class ScheduleForm(forms.ModelForm):
    """
    The `ScheduleForm` class is a form for creating and updating Schedule instances. It includes fields
    for the title, summary, duration, and URL, with customized widgets for styling.
    """
    title = forms.CharField(
        max_length=255,
        widget=Input(attrs={'class': 'h-12 rounded-lg p-2 bg-gray-900 text-white', 'placeholder': 'Title'})
    )
    summary = forms.CharField(
        max_length=1024,
        widget=Input(attrs={'class': 'h-12 rounded-lg p-2 bg-gray-900 text-white', 'placeholder': 'Description'})
    )
    duration = forms.IntegerField(
        widget=TimeInput(attrs={'class': 'h-12 rounded-lg p-2 bg-gray-900 text-white', 'placeholder': 'Duration'})
    )
    datetime = forms.DateField(
        widget=DateInput(attrs={'class': 'h-12 rounded-lg p-2 bg-gray-900 text-white', 'placeholder': 'Datetime', 'type': 'date'})
    )
    url = forms.URLField(
        widget=URLInput(attrs={'class': 'h-12 rounded-lg p-2 bg-gray-900 text-white', 'placeholder': 'URL'})
    )

    class Meta:
        model = Schedule
        fields = ['duration', 'url', 'title', 'summary', 'datetime']