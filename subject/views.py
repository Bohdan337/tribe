from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from .forms import CourseForm, AddStudentForm
from django.contrib import messages
from .models import Subject, CustomUser



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
            return redirect('/')
    else:
        form = CourseForm()
    return render(request, 'courses/create_course.html', {'form': form})



def add_student(request, subject_id):
    subject = get_object_or_404(Subject, id=subject_id)
    if request.method == 'POST':
        form = AddStudentForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            try:
                student = CustomUser.objects.get(email=email, is_student=True)
                subject.students.add(student)
                messages.success(request, 'Студента успішно додано.')
            except CustomUser.DoesNotExist:
                messages.error(request, 'Студента не знайдено або він не є студентом.')
        return redirect('subject_detail', subject_id=subject.id)
    else:
        form = AddStudentForm()
    return render(request, 'add_student.html', {'form': form, 'subject': subject})