from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from .forms import CourseForm, AddStudentForm, MaterialForm, MaterialFileForm
from .models import Subject, Material, MaterialFile
from user.models import CustomUser
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.forms import modelformset_factory







@login_required
def course(request, id):
    """
    The `course` function in Python handles the creation of materials and files for a specific subject
    in a course.
    
    :param request: The `request` parameter in the `course` function is an HttpRequest object that
    represents the current HTTP request. It contains information about the request made by the client,
    such as the request method (GET, POST, etc.), request data, user session information, and more. In
    this function, the
    :param id: The `id` parameter in the `course` function is used to identify the specific Subject
    object for which the course materials are being managed. It is used to retrieve the Subject object
    from the database using `get_object_or_404` and then associate the course materials with that
    particular subject
    :return: The `course` view function returns a rendered HTML template named 'courses/course.html'
    along with the context data containing `material_form`, `file_formset`, and `subject`.
    """
    from schedule.models import Schedule
    from schedule.forms import ScheduleForm
    from user.models import CustomUser

    subject = get_object_or_404(Subject, pk=int(id))
    MaterialFileFormSet = modelformset_factory(MaterialFile, form=MaterialFileForm, extra=1)
    materials = subject.materials.order_by("-created_at").all()

    if request.method == 'POST':

        material_form = MaterialForm(request.POST)
        file_formset = MaterialFileFormSet(request.POST, request.FILES, queryset=MaterialFile.objects.none())

        if material_form.is_valid() and file_formset.is_valid():
            material = material_form.save(commit=False)
            material.subject = subject
            material.save()

            for form in file_formset.cleaned_data:
                if form:
                    files = form['file']

                    for f in files:
                        material_file = MaterialFile(material=material, file=f)
                        material_file.save()

            messages.success(request, 'Material and files have been successfully added.')
            return redirect('course', id=subject.id)
    else:
        material_form = MaterialForm()
        file_formset = MaterialFileFormSet(queryset=MaterialFile.objects.none())

    schedules = Schedule.objects.filter(subject=subject).all()
    form = ScheduleForm()

    return render(request, 'courses/course.html', {
        'material_form': material_form,
        'file_formset': file_formset,
        'subject': subject,
        'materials': materials,
        'schedules': schedules,
        'form': form,
    })

@login_required
def students_search(request):
    from django.http import JsonResponse
    from django.template.loader import render_to_string

    if request.method == 'POST':
        search_data = request.POST.get('search')
        if search_data:
            if '@' in search_data:
                students = CustomUser.objects.filter(email__contains=search_data).all()
            else:
                students = CustomUser.objects.filter(name__contains=search_data).all()
            html = render_to_string('courses/students_search.html', {'students': students})
            print(students_search)

            return JsonResponse({'status': 'success', 'html': html})
    
    return JsonResponse({'status': 'failed', 'error': 'invalid request'}), 400

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

# --------------------------------
@login_required
def course_url(request):
    return redirect('homepage')
