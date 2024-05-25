from django.urls import path
from . import views

urlpatterns = [
    path('course/<int:id>/', views.course, name='course'),
    path('course/create/', views.create_course, name='create_course'),
]