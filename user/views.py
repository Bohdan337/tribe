
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
from django.utils.html import strip_tags
from django.core.mail import EmailMultiAlternatives


def logout(request):
    """
    The `logout` function logs out the current user in a Django web application and redirects them to
    the homepage.
    
    :param request: The `request` parameter in the `logout` function is typically an HttpRequest object
    that represents the current request from the user. It contains information about the request, such
    as user session data, headers, and other request-related information. In this context, the `logout`
    function is a part of Django
    :return: The `logout` function is being called to log out the user, and then a redirect to the
    'homepage' view is being returned.
    """
    from django.contrib.auth import logout
    logout(request)

    return redirect('homepage')



def signup(request):
    """
    The `signup` function handles user registration by creating a new user profile, sending an
    activation email, and displaying appropriate messages.
    
    :param request: The `request` parameter in the `signup` function is an object that contains
    information about the current HTTP request. It includes details such as the request method (GET,
    POST, etc.), user session data, form data, and more. In this context, the function is handling a
    user sign-up
    :return: The `signup` function returns a rendered HTML page with a form for user registration. If
    the request method is POST and the form is valid, it creates a new user and a corresponding profile,
    sends an activation email, and redirects the user to the login page with a success message. If there
    is an issue with sending the email, it redirects the user back to the signup page with an error
    message
    """
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
    """
    The `login_views` function handles user login authentication and form validation in a Django view.
    
    :param request: The `request` parameter in the `login_views` function is typically an HttpRequest
    object that represents the request made by the user to the server. It contains information about the
    request, such as the HTTP method used (GET, POST, etc.), user data, and any other relevant metadata
    :return: The `login_views` function returns a rendered template 'registration/login.html' with a
    form object if the request method is not 'POST'. If the request method is 'POST', it processes the
    form data, attempts to authenticate the user, and redirects to '/login' if the user is successfully
    authenticated.
    """
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
    """
    The `profile` function retrieves a user's profile information, subjects, and teachers, and allows
    the user to change their profile image.
    
    :param request: The `request` parameter in the `profile` function is an HttpRequest object that
    represents the current HTTP request. It contains information about the request made by the client to
    the server, such as the request method (GET, POST, etc.), headers, user data, and more. The view
    function uses
    :param slug: The `slug` parameter in the `profile` function is typically a unique identifier for a
    specific profile. It is used to retrieve the profile object from the database based on the provided
    slug value. In this case, the function is fetching the profile object with the matching slug value
    from the database using `
    :return: The `profile` function returns a rendered HTML template named 'profile.html' with the
    context data including the profile information, a form for changing the image, the subjects
    associated with the profile user, and a list of unique teacher names for those subjects. If the
    request method is POST, it also handles the form submission to change the profile image.
    """
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
    """
    The `admin_panel` function handles user search and filtering based on user type in an admin panel
    interface.
    
    :param request: The `request` parameter in the `admin_panel` function is an HttpRequest object that
    represents the request made by a user to the server. It contains information about the request, such
    as the user making the request, any data sent with the request, and other metadata related to the
    request
    :param user_type: The `user_type` parameter in the `admin_panel` function is used to filter the
    users based on their type. It can have three possible values: 'student', 'teacher', or None. If
    `user_type` is 'student', the function will retrieve only student users. If `user
    :return: The `admin_panel` function returns a rendered template named 'panel.html' with the context
    data containing the search form (`search_form`) and the list of users (`users`).
    """
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
    """
    The function `panel_user_detail` retrieves and updates user details in a panel interface.
    
    :param request: The `request` parameter in the `panel_user_detail` function is an HttpRequest object
    that Django passes to the view. It contains information about the current web request, including
    metadata, user session data, and more. This parameter allows the view to access information about
    the incoming request and interact with the user
    :param user_id: The `user_id` parameter in the `panel_user_detail` function is used to identify the
    specific user whose details are being viewed or updated. It is typically passed as part of the URL
    when accessing a user's detail page in the admin panel. The function retrieves the user object based
    on this `
    :return: The `panel_user_detail` view function is returning a rendered template
    `admin_panel/user_detail.html` with a context containing the `form` and `user` objects. The `form`
    object is either an instance of `UserUpdateForm` with the user data pre-filled for display or a new
    form if the request method is POST and the form is not valid. The `user` object is
    """
    user = get_object_or_404(CustomUser, id=user_id)
    
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'User data updated successfully')
            return redirect(request.META.get('HTTP_REFERER','/'))
    else:
        form = UserUpdateForm(instance=user)
    
    return render(request, 'admin_panel/user_detail.html', {'form': form, 'user': user})

@login_required
def delete_user(request, user_id):
    """
    The function `delete_user` deletes a user with a specific ID and redirects to the admin panel while
    displaying a success message.
    
    :param request: The `request` parameter in the `delete_user` function is typically an HttpRequest
    object that represents the current request from the user. It contains information about the request,
    such as the user's session, GET and POST data, and more. This parameter is commonly used in Django
    views to interact with the
    :param user_id: The `user_id` parameter in the `delete_user` function is the unique identifier of
    the user that you want to delete from the database. This function takes this user ID as input,
    retrieves the corresponding user object from the database using `get_object_or_404`, deletes the
    user object, displays
    :return: The `delete_user` function is returning a redirect response to the 'admin_panel' URL after
    successfully deleting the user with the specified user_id.
    """
    user = get_object_or_404(CustomUser, id=user_id)
    user.delete()
    messages.success(request, 'User deleted successfully')
    return redirect('student_panel')



def create_email(request, user, subject: str, html_page: str):
    """
    The function `create_email` generates an email message with activation token for a user account.
    
    :param request: The `request` parameter in the `create_email` function is typically an HttpRequest
    object that represents the current request from the user. It contains information about the request,
    such as headers, method, user session, and more. This parameter is commonly used in Django views to
    access request data and perform actions
    :param user: The `user` parameter in the `create_email` function is the user object for whom the
    email is being created. It likely contains information about the user such as their email address,
    name, and other relevant details
    :param subject: The `subject` parameter in the `create_email` function is a string that represents
    the subject of the email that will be sent. It is typically a brief summary or title that gives the
    recipient an idea of what the email is about. In this case, the subject is related to activating the
    user
    :type subject: str
    :param html_page: The `html_page` parameter in the `create_email` function is a string that
    represents the path to the HTML template file that will be used to generate the email content. This
    HTML template will be rendered with the provided user information and other context data to create
    the email message that will be sent to
    :type html_page: str
    :return: The `create_email` function is returning an `EmailMultiAlternatives` object that is
    configured with the provided subject, text message, and HTML message. This email object is then
    ready to be sent to the specified user's email address.
    """
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
    """
    The `activate_user` function takes a request, user ID, and token to activate a user account and
    redirects the user accordingly based on the activation status.
    
    :param request: The `request` parameter in the `activate_user` function is typically an HttpRequest
    object that represents the current request from the user's browser. It contains metadata about the
    request such as headers, method, user session, and more. This parameter allows the function to
    interact with the current request and provide a
    :param uid: The `uid` parameter in the `activate_user` function is typically the user ID encoded in
    base64 format. It is used to identify the user whose account is being activated
    :param token: The `token` parameter in the `activate_user` function is used to verify the activation
    token sent to the user for account activation. This token is generated when the user signs up and is
    included in the activation link sent to their email. The function checks if the token is valid for
    the corresponding user
    :return: The `activate_user` function is returning a redirect to the 'homepage'.
    """
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
    """
    This function handles the process of changing a user's password in a web application.
    
    :param request: The `request` parameter in the `change_password` function is an object that contains
    information about the current HTTP request. It includes details such as the user making the request,
    any data sent with the request (POST data), and other metadata related to the request. In this
    function, the `request
    :return: The `change_password` function returns a rendered template 'users/change_password.html'
    with the form data passed as context.
    """
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

    

