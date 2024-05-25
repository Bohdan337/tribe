from django.shortcuts import render, HttpResponse
from subject.models import Subject

# Create your views here.

def home(request):
    subjects = Subject.objects.all()
    context = {'subject': subjects}

    return render(request, 'index.html', context=context)