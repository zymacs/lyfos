from django.db import models
from goals.models import Goal

# Create your models here.

class Promise(models.Model):

    promise = models.CharField(max_length=1024)
    related_goals = models.ManyToManyField(Goal, blank=True)

    def __str__(self):
        return self.promise
