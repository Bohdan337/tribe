from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path('login', views.login_views, name='login'),
    path('signup', views.signup, name='signup'),
    path('logout', views.logout, name='logout'),
    path('profile/<slug:slug>', views.profile, name='profile'),
    path('users/students', views.admin_panel, {'user_type': 'student'}, name='student_panel'),
    path('users/teachers', views.admin_panel, {'user_type': 'teacher'}, name='teacher_panel'),
    path('user/<int:user_id>', views.panel_user_detail, name="user_detail"),
     path('user/<int:user_id>/delete', views.delete_user, name="delete_user"),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
