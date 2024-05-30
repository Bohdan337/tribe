
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import CustomUserCreationForm, CustomLoginForm
from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode




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
        

    email = create_email(
        request,
        user,
        'Activate your user account!',
        'users/activation.html')

    if email.send():
         messages.success(request, 'Check your email and confirm your account!')
    else:
        messages.error(request, 'Something went wrong with your email. Try it later...')
        
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



from django.utils.html import strip_tags
from django.core.mail import EmailMultiAlternatives


def create_email(request, user, subject: str, html_page: str):
    from .token import account_activation_token
    from django.contrib.sites.shortcuts import get_current_site
    # subject='Activate your email'
    message = render_to_string(html_page, {'user': user,
                                           'domain': get_current_site(request).domain,
                                           'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                                           'token': account_activation_token.make_token(user),
                                           'protocol': 'https' if request.is_secure() else 'http'}
                               )

    text_message = strip_tags(message)

    email = EmailMultiAlternatives(subject, text_message, to=[user.email])
    email.attach_alternative(message, 'text/html')
    return email

def activate_user(request, uid, token):
    from .token import account_activation_token
    from .models import CustomUser
    print('User id:', uid, 'secret token', token)
    try:
        from django.contrib.auth.models import User
        uid = force_str(urlsafe_base64_decode(uid))
        user = CustomUser.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, "Your account has been activated successfully!")
        redirect('/login')
    else:
        messages.success(request, "Invalid activation link")
    return redirect('homepage')