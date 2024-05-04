from django.shortcuts import render, HttpResponse, redirect

# Create your views here.

def login(request):
    form = ''

    return render(request, 'registration/login.html', {'form': form})

def signup(request):
    form = ''

    return render(request, 'registration/signup.html', {'form': form})

def logout(request):
    from django.contrib.auth import logout
    logout(request)

    return redirect('homepage')
