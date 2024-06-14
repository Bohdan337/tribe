from django.urls import path
from . import views


# Define the URL patterns for the application.
urlpatterns = [
    # URL pattern for creating a schedule for a specific subject. 
    # The 'subject_id' is passed as an argument to the 'create_schedule' view.
    path('schedule/<int:subject_id>', views.create_schedule, name='create_schedule'),
]