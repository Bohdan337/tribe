from django.urls import path
from . import views

urlpatterns = [
    path('course/<int:id>/', views.course, name='course'),
    path('course/search', views.students_search, name='students_search'),
    path('course/create/', views.create_course, name='create_course'),
    path('course/connect/<int:id>', views.course_url, name='connect_course'),
]