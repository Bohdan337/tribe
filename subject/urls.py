from django.urls import path
from . import views

# This code snippet is defining URL patterns for a Django application. Each `path` function call
# specifies a URL pattern along with the corresponding view function that should be called when that
# URL is accessed. Here's a breakdown of each line:
urlpatterns = [
    path('course/<int:id>/', views.course, name='course'),
    path('course/create/', views.create_course, name='create_course'),
    path('course/connect/<int:id>', views.course_url, name='connect_course'),
]