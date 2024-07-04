
from django.urls import path
from . import views

urlpatterns = [
    path('test', views.create_test, name='create_test'),
    path('test/build/<int:test_id>', views.test_build, name='test_build'),
    path('test/build/<int:test_id>/add_question', views.add_question, name='add_question'),
    path('test/<int:test_id>/publish', views.publish_test, name='publish_test'),
    path('test/<int:test_id>', views.test_detail, name='test_detail'),
]
