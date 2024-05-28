
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import CustomUserCreationForm, CustomLoginForm
from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.shortcuts import get_object_or_404




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

    profile = get_object_or_404(Profile, slug=slug)
    context = {'profile': profile}

    return render(request, 'profile.html', context=context)