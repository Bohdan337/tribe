from django import forms
from .models import Test, Question, Answer

class TestForm(forms.ModelForm):
    class Meta:
        model = Test
        fields = ['name', ]

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['question_type', 'points', 'text']

class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['text', 'is_correct', 'image']