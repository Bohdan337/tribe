from django.db import models
from user.models import CustomUser
from django.utils import timezone
from subject.models import Subject

# Create your models here.


class Schedule(models.Model):
    subject=models.ForeignKey(Subject, on_delete=models.CASCADE)
    datetime = models.DateTimeField(null=False, blank=False, default=timezone.now)
    duration = models.IntegerField(null=False, blank=False, default=0)
    link = models.TextField(null=False, blank=False, default='/link')
    
    
    def __str__(self):
        return f"{self.datetime} {self.subject}"