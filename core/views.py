from django.shortcuts import render
from subject.models import Subject
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required
def home(request):
    """
    The `home` view function retrieves all subjects from the database and renders them on the homepage.

    :param request: The HTTP request object containing request data.
    :return: A rendered HTML template displaying all subjects fetched from the database.
    """
    # Retrieve all subjects from the Subject model.
    user = request.user
    # Retrieve all subjects from the Subject model.
    subjectsStudent = Subject.objects.filter(students=user).all()
    subjectTeacher = Subject.objects.filter(teacher=user).all()

    # Render the 'index.html' template with the subjects data.
    context = {'subject': subjectsStudent,
               'subject': subjectTeacher}

    return render(request, 'index.html', context=context)
