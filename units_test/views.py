from django.shortcuts import render
from .models import Test, Question, Answer
from .forms import TestForm, QuestionForm, AnswerForm



def create_test_and_question(request):
    # Форма для створення тесту
    if request.method == 'POST' and 'create_test' in request.POST:
        test_form = TestForm(request.POST)
        if test_form.is_valid():
            # Логіка для збереження тесту
            test = test_form.save()
            return render(request, 'create_test_question.html', {'test_form': test_form, 'question_form': QuestionForm(), 'answer_forms': [AnswerForm(prefix=f'answer-{i}') for i in range(2)]})

    # Форма для створення питання з варіантами відповідей
    elif request.method == 'POST' and 'create_question' in request.POST:
        question_form = QuestionForm(request.POST)
        answer_forms = [AnswerForm(request.POST, prefix=f'answer-{i}') for i in range(2)]  # Початково два поля для варіантів відповідей

        if question_form.is_valid() and all([form.is_valid() for form in answer_forms]):
            # Логіка для збереження питання і варіантів відповідей
            question = question_form.save()
            for form in answer_forms:
                answer = form.save(commit=False)
                answer.question = question
                answer.save()
            return render(request, 'create_test_question.html', {'test_form': TestForm(), 'question_form': QuestionForm(), 'answer_forms': [AnswerForm(prefix=f'answer-{i}') for i in range(2)]})

    else:
        test_form = TestForm()
        question_form = QuestionForm()
        answer_forms = [AnswerForm(prefix=f'answer-{i}') for i in range(2)]  # Початково два поля для варіантів відповідей

    return render(request, 'test_for_student/create_test.html', {'test_form': test_form, 'question_form': question_form, 'answer_forms': answer_forms})
