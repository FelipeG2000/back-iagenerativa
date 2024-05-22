from django.db import models

# Create your models here.
class Question(models.Model):
    question = models.CharField(max_length=4096)
    def __str__(self):
        return self.question