from django.db import models
from user.models import CustomUser
from subject.models import Subject

# Create your models here.


class Schedule(models.Model):
    day=models.TextField(max_length=300, blank=True, null=True)
    subject=models.ForeignKey(Subject, on_delete=models.CASCADE)
    #grade=models.CharField(max_length=200, null=True)
    start_time=models.TimeField(max_length=200, null=True)
    end_time=models.TimeField(max_length=200, null=True)
    students=models.ForeignKey(CustomUser, on_delete=models.DO_NOTHING)
    
    def __str__(self):
        return f"{self.day} {self.subject} {self.start_time} {self.end_time}"