
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import CustomUserCreationForm, CustomLoginForm
from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.shortcuts import get_object_or_404, get_list_or_404
from .forms import UserSearchForm
from .models import CustomUser



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
            
            print(user, password)
            if user is not None:
                auth_login(request, user)
                messages.success(request, f'Logged in successfully, {user.name}.')
                return redirect('/')

    else:
        form = CustomLoginForm()
    return render(request, 'registration/login.html', {'form': form})



def profile(request, slug):
    from .models import Profile
    from .forms import ChangeImageForm
    from subject.models import Subject

    profile = get_object_or_404(Profile, slug=slug)
    
    subjects = get_list_or_404(Subject, students=profile.user)

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


@login_required
def admin_panel(request):
    if not request.user.is_chief_teacher or not request.user.is_superuser:
        messages.info(request, 'You are not authorized to admin panel.')
        return redirect('homepage')

    form = UserSearchForm()
    users = CustomUser.objects.all()  

    if 'email' in request.GET:
        form = UserSearchForm(request.GET)
        if form.is_valid():
            email = form.cleaned_data['email']
            if email:
                try:
                    user = CustomUser.objects.get(email=email)
                    users = [user]
                except CustomUser.DoesNotExist:
                    users = CustomUser.objects.all()  
                    messages.error(request, 'Користувача не знайдено')
            else:
                users = CustomUser.objects.all()

    return render(request, 'admin_panel/panel.html', {'search_form': form, 'users': users})