from django.urls import path
from . import views


urlpatterns = [
    path('schedule/create/', views.create_schedule, name='create_schedule')
]