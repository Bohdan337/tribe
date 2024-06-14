from django.shortcuts import render
from subject.models import Subject
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required
def home(request):
    # user = request.user
    # subjects = Subject.objects.filter(students__in=user).distinct()
    # print(subjects)

    subjects = Subject.objects.all()
    context = {'subject': subjects}

    return render(request, 'index.html', context=context)

