from django.shortcuts import render, HttpResponse, redirect

# Create your views here.

def login(request):
    from .forms import LoginForm

    form = LoginForm()

    return render(request, 'registration/login.html', {'form': form})

def signup(request):
    from .forms import SignupForm

    if request.method == 'POST':
        form = SignupForm(request = request.POST)
        user = form.save()
        print(f'\v\t{user.username}\v') 

    form = SignupForm()

    return render(request, 'registration/signup.html', {'form': form})

def logout(request):
    from django.contrib.auth import logout
    logout(request)

    return redirect('homepage')
