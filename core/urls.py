from django.urls import path

from . import views


# Define the URL patterns for your Django application.
urlpatterns = [
    # URL pattern for the homepage, which maps to the `home` view function in the `views` module.
    path('', views.home, name='homepage'),
]