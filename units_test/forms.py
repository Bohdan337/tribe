from django import forms
from .models import Test, Question, Answer
from subject.models import Subject


class TestForm(forms.ModelForm):
    class Meta:
        model = Test
        fields = ['name', 'subject']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'm-2 h-36 rounded-lg p-2 bg-gray-900 text-white', 'placeholder': "test's name.."}), 
            'subject': forms.Select(attrs={'class': 'm-2 h-36 rounded-lg p-2 bg-gray-900 text-white', 'style': 'width: 25rem'})
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(TestForm, self).__init__(*args, **kwargs)
        if user:
            self.fields['subject'].queryset = Subject.objects.filter(teacher=user)



class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['question_type', 'points', 'text']
        widgets = {
            'question_type': forms.Select(attrs={'class': 'm-2 h-36 rounded-lg p-2 bg-gray-900 text-white', 'style': 'width: 25rem'}),
            'text': forms.Textarea(attrs={'class': 'm-2 rounded-lg p-2 bg-gray-900 text-white', 'placeholder': "your question", 'cols': '20', 'rows': '5'}), 
            'points': forms.NumberInput(attrs={'class': 'm-2 h-36 rounded-lg p-2 bg-gray-900 text-white', 'placeholder': "points"}), 
        }

class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['is_correct', 'text', 'image']
        widgets = {
            'text': forms.TextInput(attrs={'class': 'm-2 h-36 rounded-lg p-2 bg-gray-900 text-white', 'placeholder': "test's name.."}), 
        }