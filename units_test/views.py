from django.shortcuts import render
from .models import Test, Question, Answer
from .forms import TestForm, QuestionForm, AnswerForm



def create_test_and_question(request):
    
    test_form = TestForm()
    question_form = QuestionForm()
    answer_forms = AnswerForm ()

    return render(request, 'test_for_student/create_test.html', {'test_form': test_form, 'question_form': question_form, 'answer_forms': answer_forms})
