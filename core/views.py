from django.shortcuts import render
from subject.models import Subject
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required
def home(request):
    user = request.user
    subjectsStudent = Subject.objects.filter(students=user).all()
    subjectTeacher = Subject.objects.filter(teacher=user).all()

    # subjects = Subject.objects.all()
    context = {'subject': subjectsStudent,
               'subject': subjectTeacher}

    return render(request, 'index.html', context=context)

