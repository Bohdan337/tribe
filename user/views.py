
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
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str


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
            
            email = create_email(
                request,
                user,
                'Activate your user account!',
                'users/activation.html')

            if email.send():
                messages.success(request, 'Check your email and confirm your account!')
                return redirect('login')
            else:
                messages.error(request, 'Something went wrong with your email. Try it later...')
                return redirect('signup')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})



def login_views(request):
    if request.method == 'POST':
        form = CustomLoginForm(request, data=request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=form.cleaned_data.get('username'),
                                password=form.cleaned_data.get('password')) 
            
            
            
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
def admin_panel(request, user_type=None):
    if request.user.is_student:
        return redirect('homepage')
    
    form = UserSearchForm()
    
    if user_type == 'student':
        users = CustomUser.objects.filter(is_student=True)
    elif user_type == 'teacher':
        users = CustomUser.objects.filter(is_teacher=True)
    else:
        users = CustomUser.objects.all()

    if 'email' in request.POST:
        form = UserSearchForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            if email:
                try:
                    user = CustomUser.objects.get(email=email)
                    users = [user]
                except CustomUser.DoesNotExist:
                    if user_type == 'student':
                        users = CustomUser.objects.filter(is_student=True)
                    elif user_type == 'teacher':
                        users = CustomUser.objects.filter(is_teacher=True)
                    else:
                        users = CustomUser.objects.all()
                    messages.error(request, 'User not found')
            else:
                if user_type == 'student':
                    users = CustomUser.objects.filter(is_student=True)
                elif user_type == 'teacher':
                    users = CustomUser.objects.filter(is_teacher=True)
                else:
                    users = CustomUser.objects.all()

    return render(request, 'admin_panel/panel.html', {'search_form': form, 'users': users})




@login_required
def panel_user_detail(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'User data updated successfully')
            return redirect(request.meta['HTTP_REFERRER'])
    else:
        form = UserUpdateForm(instance=user)
    
    return render(request, 'admin_panel/user_detail.html', {'form': form, 'user': user})

@login_required
def delete_user(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    user.delete()
    messages.success(request, 'User deleted successfully')
    return redirect('admin_panel')


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


@login_required
def change_password(request):
    from .forms import UpdatePasswordForm

    form = UpdatePasswordForm(request.user)
    if request.method == 'POST':
        form = UpdatePasswordForm(request.user, request.POST)
        if request.method == 'POST':
            form = UpdatePasswordForm(request.user, request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'Your password has been changed!')

                return redirect('login')
            else:
                for key, error in list(form.errors.items()):
                    if key == 'captcha' and error[0] == 'This field is required.':
                        messages.error(request, 'Please complete the ReCaptcha!')
                        continue
                    messages.error(request, error)

    return render(request, 'users/change_password.html', {'form': form})

    

