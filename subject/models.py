from django.db import models
from user.models import CustomUser

# Create your models here.

    
class Subject(models.Model):
    title = models.CharField(max_length=200, null=True)
    teacher = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    summary = models.TextField(max_length=300, blank=True, null=True)
    grade = models.CharField(max_length=5, null=True)
    # term = models.CharField(max_length=200, null=True)
    
    def __str__(self):
        return f"{self.title} {self.teacher} ({self.grade})"
    