from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.core.validators import EmailValidator



import datetime
class CustomUser(AbstractUser):
    is_student = models.BooleanField(default=True)
    is_teacher = models.BooleanField(default=False)
    is_chief_teacher = models.BooleanField(default=False)

    groups = models.ManyToManyField(Group, verbose_name=('groups'), blank=True, related_name='customuser_set', related_query_name='user')
    user_permissions = models.ManyToManyField(Permission, verbose_name=('user permissions'), blank=True, related_name='customuser_set', related_query_name='user')
    email=models.EmailField(null=False, blank=False, unique=True)
    name=models.CharField(null=False, max_length=50, default='name')
    surname=models.CharField(null=False, max_length=50, default='surname')
    created_at=models.DateTimeField(default=datetime.datetime.now())

    
    

