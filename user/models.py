from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.core.validators import EmailValidator




class CustomUser(AbstractUser):
    is_student = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)
    is_chief_teacher = models.BooleanField(default=False)

    groups = models.ManyToManyField(Group, verbose_name=('groups'), blank=True, related_name='customuser_set', related_query_name='user')
    user_permissions = models.ManyToManyField(Permission, verbose_name=('user permissions'), blank=True, related_name='customuser_set', related_query_name='user')



class Student(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True, related_name='student')
    name = models.CharField(max_length=100, blank=True)
    surname = models.CharField(max_length=150, blank=True)
    email = models.EmailField(unique=True, validators=[EmailValidator()], blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} {self.surname} ({self.email})"
    



class Teacher(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True, related_name='teacher')
    name = models.CharField(max_length=100, blank=True)
    surname = models.CharField(max_length=150, blank=True)
    email = models.EmailField(unique=True, validators=[EmailValidator()], blank=True)

    achievements = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} {self.surname} ({self.email})"

class ChiefTeacher(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True, related_name='chiefteacher')
    name = models.CharField(max_length=100, blank=True)
    surname = models.CharField(max_length=150, blank=True)
    email = models.EmailField(unique=True, validators=[EmailValidator()], blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    teachers = models.ManyToManyField(Teacher, blank=True)
    
    def __str__(self):
        return f"{self.name} {self.surname} ({self.email})"
    
    
    
    
class Classes(models.Model):
    tittle = models.CharField(max_length=200, null=True)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    summary = models.TextField(max_length=300, blank=True, null=True)
    grade = models.CharField(max_length=5, null=True)
    term = models.CharField(max_length=200, null=True)
    
    def __str__(self):
        return f"{self.tittle} {self.teacher} ({self.grade})"
    
    
class Schedule(models.Model):
    day=models.TextField(max_length=300, blank=True, null=True)
    lessons=models.ForeignKey(Classes, on_delete=models.CASCADE)
    grade=models.CharField(max_length=200, null=True)
    start_time=models.CharField(max_length=200, null=True)
    end_time=models.CharField(max_length=200, null=True)
    
    def __str__(self):
        return f"{self.day} {self.lessons} {self.start_time} {self.end_time}"
    

class Grade(models.Model):
    grade_id=models.CharField(max_length=245, null=False, blank=False)
    grade_tittle=models.CharField(max_length=245, null=False, blank=False)
    grade_leader=models.ForeignKey(Teacher, on_delete=models.CASCADE)
