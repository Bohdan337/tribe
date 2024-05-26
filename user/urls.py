from django.urls import path

from . import views

urlpatterns = [
    path('login', views.login_views, name='login'),
    path('signup', views.signup, name='signup'),
    path('logout', views.logout, name='logout'),
    path('profile/<slug:slug>', views.profile, name='profile'),
]
