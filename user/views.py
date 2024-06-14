
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import CustomUserCreationForm, CustomLoginForm
from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.shortcuts import get_object_or_404, get_list_or_404
from django.contrib.auth.decorators import login_required




def logout(request):
    from django.contrib.auth import logout
    logout(request)

    return redirect('homepage')



def signup(request):
    from . models import Profile

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()

            profile = Profile(user=user)
            profile.save()

            print(profile)

            messages.success(request, f'Account created successfully, {user.name}. You can now log in.')
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})



def login_views(request):
    if request.method == 'POST':
        form = CustomLoginForm(request, data=request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=email, password=password) 
            

            if user is not None:
                auth_login(request, user)
                messages.success(request, f'Logged in successfully, {user.name}.')
                return redirect('/')

    else:
        form = CustomLoginForm()
    return render(request, 'registration/login.html', {'form': form})


@login_required
def profile(request, slug):
    from .models import Profile
    from .forms import ChangeImageForm
    from subject.models import Subject

    profile = get_object_or_404(Profile, slug=slug)
    
    subjects = Subject.objects.filter(students=request.user).all()

    teachers = []
    for subject in subjects:
        teachers.append(subject.teacher.name)
    res = []
    [res.append(x) for x in teachers if x not in res]

    form = ChangeImageForm()

    context = {'profile': profile,
               'form': form,
               'subjects': subjects,
               'teachers': res}
    
    if request.method == "POST":
        form = ChangeImageForm(request.POST, request.FILES)
        if form.is_valid():
            profile.image = form.cleaned_data.get('image')
            profile.save()

    return render(request, 'profile.html', context=context)