from django.db import models
from user.models import CustomUser

# Create your models here.

    
# This class defines a Subject model with fields for title, teacher, summary, grade, and students,
# along with methods for string representation.
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
    
    

# The `Material` class defines a model with fields for subject, title, description, and creation
# timestamp.
class Material(models.Model):
    subject = models.ForeignKey(Subject, related_name="materials", on_delete=models.CASCADE)
    title = models.CharField(max_length=250, null=False, blank=False)
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


# The `MaterialFile` class represents a model with fields for a material, file, and creation timestamp
# in a Django application.
class MaterialFile(models.Model):
    material = models.ForeignKey(Material, related_name='files', on_delete=models.CASCADE)
    file = models.FileField(upload_to='materials/%Y/%m/%d')
    created_at = models.DateTimeField(auto_now_add=True)
    


class Grade(models.Model):
    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='grades')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='grades')
    grade = models.DecimalField(max_digits=5, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Grade {self.grade} for {self.student.name} in {self.subject.title}'