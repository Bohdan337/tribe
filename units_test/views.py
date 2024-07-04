from django.shortcuts import render, redirect, get_object_or_404
from .models import Test, Question, Answer
from .forms import TestForm, QuestionForm, AnswerForm
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from subject.models import Subject

def create_test(request):
    if request.method == 'POST':
        form = TestForm(request.POST)
        if form.is_valid():
            form_data = form.cleaned_data
            form_data['subject'] = form_data['subject'].id  # Зберігаємо лише ID предмета

            # Отримуємо або ініціалізуємо лічильник ID тестів в сесії
            if 'test_counter' not in request.session:
                request.session['test_counter'] = 0

            # Інкрементуємо лічильник і використовуємо його як ID тесту
            request.session['test_counter'] += 1
            test_id = request.session['test_counter']

            form_data['id'] = test_id
            request.session[f'test_{test_id}'] = form_data  # Зберігаємо дані форми в сесії

            return redirect('test_build', test_id=test_id)  # Перенаправляємо на сторінку побудови тесту з ID тесту
    else:
        form = TestForm()

    return render(request, 'test_for_student/create_test.html', {'test_form': form})

def test_build(request, test_id):
    test_data = request.session.get(f'test_{test_id}', {})
    if test_data:
        test_data['subject'] = get_object_or_404(Subject, id=test_data['subject'])
    questions = request.session.get(f'questions_{test_id}', [])
    total_points = sum(question['points'] for question in questions)

    question_form = QuestionForm()
    answer_forms = [AnswerForm(prefix=str(i)) for i in range(3)]

    return render(request, 'test_for_student/test_build.html', {
        'test_data': test_data,
        'questions': questions,
        'question_form': question_form,
        'answer_forms': answer_forms,
        'total_points' : total_points
    })

@csrf_exempt
def add_question(request, test_id):
    if request.method == 'POST':
        question_form = QuestionForm(request.POST)
        answer_forms = [AnswerForm(request.POST, prefix=str(i)) for i in range(3)]  # Приклад для трьох відповідей

        if question_form.is_valid() and all([af.is_valid() for af in answer_forms]):
            question_data = question_form.cleaned_data
            question_data['answers'] = [af.cleaned_data for af in answer_forms]

            questions = request.session.get(f'questions_{test_id}', [])
            questions.append(question_data)
            request.session[f'questions_{test_id}'] = questions

            return JsonResponse({'success': True})
        else:
            errors = question_form.errors
            for af in answer_forms:
                errors.update(af.errors)
            return JsonResponse({'success': False, 'errors': errors})
    return JsonResponse({'success': False, 'errors': 'Invalid request method'})

def publish_test(request, test_id):
    if request.method == 'POST':
        test_data = request.session.get(f'test_{test_id}', {})
        questions = request.session.get(f'questions_{test_id}', [])

        if test_data and questions:
            subject = get_object_or_404(Subject, id=test_data['subject'])
            test = Test(
                name=test_data['name'],
                subject=subject,
                teacher=request.user
            )
            test.save()

            for question_data in questions:
                question = Question(
                    test=test,  # Assign the test instance to the test field
                    question_type=question_data['question_type'],
                    points=question_data['points'],
                    text=question_data['text']
                )
                question.save()

                for answer_data in question_data['answers']:
                    answer = Answer(
                        question=question,
                        is_correct=answer_data['is_correct'],
                        text=answer_data['text'],
                        image=answer_data.get('image', None)  # image може бути відсутнім
                    )
                    answer.save()

            # Очистимо сесію після збереження
            del request.session[f'test_{test_id}']
            del request.session[f'questions_{test_id}']

            return redirect('test_detail', test_id=test.pk)

    return redirect('test_build', test_id=test_id)


def test_detail(request, test_id):
    test = get_object_or_404(Test, id=test_id)
    return render(request, 'test_for_student/test_detail.html', {'test': test})
