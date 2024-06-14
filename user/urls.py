from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

# This code block in a Django project is defining the URL patterns for different views in the
# application. Each `path` function call specifies a URL pattern along with the corresponding view
# function that should be called when that URL is accessed. Here's a breakdown of what each path is
# doing:
urlpatterns = [
    path('login', views.login_views, name='login'),
    path('signup', views.signup, name='signup'),
    path('logout', views.logout, name='logout'),
    path('profile/<slug:slug>', views.profile, name='profile'),
    path('panel', views.admin_panel, name="admin_panel"),
    path('panel/user/<int:user_id>/', views.panel_user_detail, name="user_detail"),
     path('panel/user/<int:user_id>/delete/', views.delete_user, name="delete_user"),
    path('profile/password/change', views.change_password, name='change_user_password'),
    path('activate/<uid>/<token>', views.activate_user, name='activate_user'),

    path('users/students', views.admin_panel, {'user_type': 'student'}, name='student_panel'),
    path('users/teachers', views.admin_panel, {'user_type': 'teacher'}, name='teacher_panel'),
    path('user/<int:user_id>', views.panel_user_detail, name="user_detail"),
     path('user/<int:user_id>/delete', views.delete_user, name="delete_user"),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
