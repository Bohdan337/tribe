from django.db import models
from user.models import Teacher

class Grade(models.Model):
    grade_id=models.CharField(max_length=245, null=False, blank=False)
    grade_tittle=models.CharField(max_length=245, null=False, blank=False)
    grade_leader=models.ForeignKey(Teacher, on_delete=models.CASCADE)
