
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import CustomUserCreationForm, StudentForm, TeacherForm, ChiefTeacherForm
from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login



def logout(request):
    from django.contrib.auth import logout
    logout(request)

    return redirect('homepage')



def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid email or password')
    return render(request, 'registration/login.html')



def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            if 'student_signup' in request.POST:
                student_form = StudentForm(request.POST)
                if student_form.is_valid():
                    user.is_student = True
                    student = student_form.save(commit=False)
                    student.user = user
                    student.save()
            elif 'teacher_signup' in request.POST:
                teacher_form = TeacherForm(request.POST)
                if teacher_form.is_valid():
                    user.is_teacher = True
                    teacher = teacher_form.save(commit=False)
                    teacher.user = user
                    teacher.save()
            messages.success(request, 'Account created successfully. You can now log in.')
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})