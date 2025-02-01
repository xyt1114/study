from django.db import models

# Create your models here.
class Job(models.Model):
    title = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    salary = models.CharField(max_length=100)
    sign = models.IntegerField(default=4)

class Occupation(models.Model):
    title = models.CharField(max_length=100)
    salary = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    experience = models.CharField(max_length=100)
    educational_background = models.CharField(max_length=100)
    job_description = models.CharField(max_length=100)
    tech_stack = models.CharField(max_length=100)