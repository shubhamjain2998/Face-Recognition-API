from django.db import models

# Create your models here.
class Employee(models.Model):
    ID = models.IntegerField(primary_key=True)
    Name = models.CharField(max_length=50)
