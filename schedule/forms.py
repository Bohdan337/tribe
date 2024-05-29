from django import forms
from .models import Schedule
from django.forms.widgets import Input
from user.models import CustomUser


class ScheduleForm(forms.ModelForm):

    class Meta:
        model = Schedule
        fields = ['duration', 'link']