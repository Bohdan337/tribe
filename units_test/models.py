from django.db import models
from user.models import CustomUser
from subject.models import Subject


class Test(models.Model):
    name = models.CharField(max_length=255)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, max_length=255)
    teacher = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='tests')

    def __str__(self):
        return self.name


         
class Question(models.Model):
    SINGLE_ANSWER = 'single'
    MULTIPLE_ANSWERS = 'multiple'
    ANSWER_TYPE_CHOICES = [
        (SINGLE_ANSWER, 'One correct answer'),
        (MULTIPLE_ANSWERS, 'Several correct answers'), 
    ]

    test = models.ForeignKey(Test, on_delete=models.CASCADE, related_name='questions')
    question_type = models.CharField(max_length=10, choices=ANSWER_TYPE_CHOICES, default=SINGLE_ANSWER)
    points = models.IntegerField(default=1)
    text = models.TextField()

    def __str__(self):
        return self.text

class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    is_correct = models.BooleanField(default=False)
    text = models.TextField()
    image = models.ImageField(upload_to='question_images/', blank=True, null=True)


    def __str__(self):
        return self.text
