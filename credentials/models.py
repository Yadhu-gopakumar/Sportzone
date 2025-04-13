from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class userprofile(models.Model):
    name=models.CharField(max_length=100)
    email=models.CharField(max_length=200)
    

class ownerprofile(models.Model):
    
    name=models.CharField(max_length=100)
    email=models.CharField(max_length=200)
    phone=models.CharField(max_length=15)
  