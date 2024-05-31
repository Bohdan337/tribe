from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from .forms import CourseForm, AddStudentForm
from .models import Subject
from user.models import CustomUser
from django.contrib import messages
from django.shortcuts import get_object_or_404

@login_required
def course(request, id):
    from .models import Subject
    from schedule.models import Schedule
    from schedule.forms import ScheduleForm

    subject = get_object_or_404(Subject, pk=int(id))
    schedules = Schedule.objects.filter(subject=subject).all()
    print(schedules)
    form = ScheduleForm()

    context = {'subject': subject,
               'schedules': schedules,
               'form': form}

    return render(request, 'courses/course.html', context=context)

@login_required
def create_course(request):
    if not request.user.is_teacher:
        messages.info(request, 'You are not authorized to create a course.')
        return redirect('homepage')

    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            course = form.save(commit=False)
            course.teacher = request.user
            
            course.save()
            form.save_m2m()
            print(course)

            messages.success(request, 'Course created successfully.')
            return redirect('/')
    else:
        form = CourseForm()
    return render(request, 'courses/create_course.html', {'form': form})

@login_required
def course_url(request, id):
    from .models import Subject
    course = get_object_or_404(Subject, pk=id)
    course.students.add(request.user)
    course.save()
    print(course.students.all())

    return redirect('course', id=id)



# def add_student(request, subject_id):
#     subject = get_object_or_404(Subject, id=subject_id)
#     if request.method == 'POST':
#         form = AddStudentForm(request.POST)
#         if form.is_valid():
#             email = form.cleaned_data['email']
#             try:
#                 student = CustomUser.objects.get(email=email, is_student=True)
#                 subject.students.add(student)
#                 messages.success(request, 'Студента успішно додано.')
#             except CustomUser.DoesNotExist:
#                 messages.error(request, 'Студента не знайдено або він не є студентом.')
#         return redirect('subject_detail', subject_id=subject.id)
#     else:
#         form = AddStudentForm()
#     return render(request, 'add_student.html', {'form': form, 'subject': subject})