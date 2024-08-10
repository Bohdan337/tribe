from django.shortcuts import render, redirect, get_object_or_404
from .models import Test, Question, Answer
from .forms import TestForm, QuestionForm, AnswerForm
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse,QueryDict
from subject.models import Subject

def create_test(request):
    if request.method == 'POST':
        form = TestForm(request.POST)
        if form.is_valid():
            form_data = form.cleaned_data
            form_data['subject'] = form_data['subject'].id  

           
            if 'test_counter' not in request.session:
                request.session['test_counter'] = 0

           
            request.session['test_counter'] += 1
            test_id = request.session['test_counter']

            form_data['id'] = test_id
            request.session[f'test_{test_id}'] = form_data 

            return redirect('test_build', test_id=test_id)  
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

def delete_question(request, test_id, question_index):
    if request.method == 'POST':
        try:
            questions = request.session.get(f'questions_{test_id}', [])
            if 0 <= question_index < len(questions):
                del questions[question_index]
                request.session[f'questions_{test_id}'] = questions
                return JsonResponse({'status': 'success'})
            else:
                return JsonResponse({'status': 'failed', 'error': 'invalid question index'}, status=400)
        except Exception as e:
            return JsonResponse({'status': 'failed', 'error': str(e)}, status=400)
    else:
        return JsonResponse({'status': 'failed', 'error': 'invalid request method'}, status=400)

@csrf_exempt
def add_question(request, test_id):
    if request.method == 'POST':
        question_form = QuestionForm(request.POST)
        answer_forms = [AnswerForm(request.POST, prefix=str(i)) for i in range(3)]  

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
                    test=test,  
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
                        image=answer_data.get('image', None)  
                    )
                    answer.save()

            del request.session[f'test_{test_id}']
            del request.session[f'questions_{test_id}']

            return redirect('test_detail', test_id=test.pk)

    return redirect('test_build', test_id=test_id)  


def test_detail(request, test_id):
    test = get_object_or_404(Test, id=test_id)
    questions = Question.objects.filter(test=test)
    
    return render(request, 'test_for_student/test_detail.html', {'test': test, 'questions': questions})