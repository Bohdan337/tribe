from django.urls import path
from . import views

urlpatterns = [
    path('course/<int:id>/', views.course, name='course'),
    path('course/create/', views.create_course, name='create_course'),
    path('subject/<int:subject_id>/add_student/', views.add_student, name='add_student'),
]