from django.db import models
from user.models import CustomUser

# Create your models here.

    
class Subject(models.Model):
    title = models.CharField(max_length=200, null=True)
    teacher = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    summary = models.TextField(max_length=300, blank=True, null=True)
    grade = models.CharField(max_length=5, null=True)
    students = models.ManyToManyField(CustomUser, limit_choices_to={'is_student': True},
                                       related_name='students', blank=True, null=True)
    # term = models.CharField(max_length=200, null=True)
    # created_at = models.DateTimeField(auto_now_add=True)
    
    
    def __str__(self):
        return f"{self.title} {self.teacher} ({self.grade}) {self.students.all()}"
    
    def __repr__(self):
        return f"{self.title} {self.teacher} ({self.grade}) {self.students.all()}"
    
    

class Material(models.Model):
    subject = models.ForeignKey(Subject, related_name="materials", on_delete=models.CASCADE)
    title = models.CharField(max_length=250, null=False, blank=False)
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


class MaterialFile(models.Model):
    material = models.ForeignKey(Material, related_name='files', on_delete=models.CASCADE)
    file = models.FileField(upload_to='materials/%Y/%m/%d')
    created_at = models.DateTimeField(auto_now_add=True)

    
    