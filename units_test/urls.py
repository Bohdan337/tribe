
from django.urls import path
from . import views

urlpatterns = [
    path('test/', views.create_test_and_question, name='create_test_and_question'),
]