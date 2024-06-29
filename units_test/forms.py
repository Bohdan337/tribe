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

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['question_type', 'points', 'text']

class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['text', 'is_correct', 'image']