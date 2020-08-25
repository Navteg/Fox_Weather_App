from django.db import models
from . import views
# Create your models here.
class Data(models.Model):
    city = models.CharField(max_length=50)
    temp = models.CharField(max_length=10)
