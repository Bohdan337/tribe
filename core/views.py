from django.shortcuts import render, HttpResponse
from subject.models import Subject

def home(request):
    """
    The `home` view function retrieves all subjects from the database and renders them on the homepage.

    :param request: The HTTP request object containing request data.
    :return: A rendered HTML template displaying all subjects fetched from the database.
    """
    # Retrieve all subjects from the Subject model.
    subjects = Subject.objects.all()
    # Prepare the context dictionary with subjects to be passed to the template.
    context = {'subjects': subjects}
    # Render the 'index.html' template with the subjects data.
    return render(request, 'index.html', context=context)
