from django.urls import path
from . import views


urlpatterns = [
    path('schedule/<int:subject_id>', views.create_schedule, name='create_schedule')
]