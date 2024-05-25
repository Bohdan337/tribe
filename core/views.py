from django.shortcuts import render, HttpResponse
from subject.models import Subject

# Create your views here.

def home(request):
    courses = Subject.objects.all()
    context = {'courses': courses}
    print(courses)

    return render(request, 'index.html', context=context)

