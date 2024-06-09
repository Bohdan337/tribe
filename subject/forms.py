from django import forms
from .models import Subject, Material, MaterialFile
from django.forms.widgets import Input
from user.models import CustomUser
from tinymce.widgets import TinyMCE



class CourseForm(forms.ModelForm, forms.Form):
    title = forms.CharField(max_length=255, widget=Input(attrs={'class': 'm-3 h-12 rounded-lg p-2 bg-gray-900 text-white', 'placeholder': 'Title'}))
    summary = forms.CharField(max_length=1024, widget=Input(attrs={'class': 'm-3 h-12 rounded-lg p-2 bg-gray-900 text-white', 'placeholder': 'Description'}))
    students = forms.ModelMultipleChoiceField(queryset=CustomUser.objects.filter(is_student=True, is_superuser=False), widget=forms.CheckboxSelectMultiple())

    class Meta:
        model = Subject
        fields = ['title', 'summary', 'students']



class AddStudentForm(forms.Form):
    students = forms.ModelMultipleChoiceField(queryset=CustomUser.objects.filter(is_student=True, is_superuser=False), widget=forms.CheckboxSelectMultiple())

    class Meta:
        model = Subject
        fields = ['students']



class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = [single_file_clean(data, initial)]
        return result




class MaterialForm(forms.ModelForm):
    title = forms.CharField(max_length=255, widget=Input(attrs={'class': 'h-12 rounded-lg p-2 bg-gray-900 text-white w-96', 'placeholder': 'Title'}))
    description = forms.CharField(widget=TinyMCE(attrs={
        'class': 'm-2 h-12 rounded-lg p-2 bg-gray-900 text-white', 
        'placeholder': 'Description'
    }))

    class Meta:
        model = Material
        fields = ['title', 'description']


class MaterialFileForm(forms.ModelForm):
    file = MultipleFileField()

    class Meta:
        model = MaterialFile
        fields = ['file']
        # widgets = {'file' : forms.ClearableFileInput(attrs={'allow_multiple_selected': True})}




