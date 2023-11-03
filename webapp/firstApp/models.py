from django.db import models

#import .models from internship

# Create your models here.

class internship(models.Model):
    age = models.FloatField()
    sex = models.FloatField()
    bmi = models.FloatField()
    children = models.FloatField()
    smoker = models.FloatField()
    region = models.FloatField()
    charges = models.FloatField()