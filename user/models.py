from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission




class CustomUser(AbstractUser):
    is_student = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)
    is_chief_teacher = models.BooleanField(default=False)

    groups = models.ManyToManyField(Group, verbose_name=('groups'), blank=True, related_name='customuser_set', related_query_name='user')
    user_permissions = models.ManyToManyField(Permission, verbose_name=('user permissions'), blank=True, related_name='customuser_set', related_query_name='user')



class Student(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True, related_name='student', default=None)
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=150)
    email = models.EmailField(unique=True)

    created_at = models.DateTimeField(auto_now_add=True)
    # subjects_studied = models.ManyToManyField('Subject', blank=True)


    def __str__(self):
        return f"{self.name} {self.surname}"




class Teacher(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True, related_name='teacher', default=None)
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=150)
    email = models.EmailField(unique=True)

    achievements = models.TextField(blank=True, null=True)
    # subjects_taught = models.ManyToManyField('Subject', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"{self.name} {self.surname}"




class ChiefTeacher(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True, related_name='chiefteacher', default=None)
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    # subjects_assigned = models.ManyToManyField('Subject', blank=True)
    teachers = models.ManyToManyField(Teacher, blank=True)


    def __str__(self):
        return f"{self.name} {self.surname}"