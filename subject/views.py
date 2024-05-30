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
            form.save_m2m()
            print(course)

            messages.success(request, 'Course created successfully.')
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




def save_material(request, subject_id):
    subject = get_object_or_404(Subject, id=subject_id)
    MaterialFileFormSet = modelformset_factory(MaterialFile, form=MaterialFileForm, extra=3)  # Adjust 'extra' as needed

    if request.method == 'POST':
        material_form = MaterialForm(request.POST)
        file_formset = MaterialFileFormSet(request.POST, request.FILES, queryset=MaterialFile.objects.none())

        if material_form.is_valid() and file_formset.is_valid():
            material = material_form.save(commit=False)
            material.subject = subject
            material.save()

            for form in file_formset.cleaned_data:
                if form:
                    file = form['file']
                    material_file = MaterialFile(material=material, file=file)
                    material_file.save()

            return redirect('subject_detail', subject_id=subject.id)
    else:
        material_form = MaterialForm()
        file_formset = MaterialFileFormSet(queryset=MaterialFile.objects.none())

    return render(request, 'upload_material.html', {
        'material_form': material_form,
        'file_formset': file_formset,
        'subject': subject
    })








