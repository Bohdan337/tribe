from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from .forms import CourseForm
from django.contrib import messages
from django.shortcuts import get_object_or_404

@login_required
def course(request, id):
    from .models import Subject
    subject = get_object_or_404(Subject, pk=int(id))
    context = {'subject': subject}

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
            return redirect('/')
    else:
        form = CourseForm()
    return render(request, 'courses/create_course.html', {'form': form})