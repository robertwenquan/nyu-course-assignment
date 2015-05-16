from django.db import models

# Create your models here.
class OptimalPath(models.Model):
  hashkey = models.CharField(max_length=32)
  path = models.CharField(max_length=256)
