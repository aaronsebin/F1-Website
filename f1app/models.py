# Create your models here.
from django.db import models


class Driver(models.Model):
    name = models.CharField(max_length=100)
    team = models.CharField(max_length=100)
    nationality = models.CharField(max_length=100)
    points = models.FloatField(default=0)

    def __str__(self):
        return self.name