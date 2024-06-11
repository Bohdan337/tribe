
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import CustomUserCreationForm, CustomLoginForm, UserSearchForm, UserUpdateForm
from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.shortcuts import get_object_or_404, get_list_or_404
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




def chief_teacher_required(view_func):
    def wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')  
        if not (request.user.is_chief_teacher or request.user.is_superuser):
            messages.info(request, 'You are not authorized to access the admin panel.')
            return redirect('homepage')  
        return view_func(request, *args, **kwargs)
    return wrapped_view



@chief_teacher_required
def admin_panel(request):
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
                    messages.error(request, 'User not found')
            else:
                users = CustomUser.objects.all()

    return render(request, 'admin_panel/panel.html', {'search_form': form, 'users': users})

@chief_teacher_required
def panel_user_detail(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'User data updated successfully')
            return redirect('admin_panel')
    else:
        form = UserUpdateForm(instance=user)
    
    return render(request, 'admin_panel/user_detail.html', {'form': form, 'user': user})

@chief_teacher_required
def delete_user(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    user.delete()
    messages.success(request, 'User deleted successfully')
    return redirect('admin_panel')