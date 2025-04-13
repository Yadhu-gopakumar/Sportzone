from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class turf_table(models.Model):
   
    image=models.ImageField(default="turfimages/img.png",upload_to='turfimages')
    ownername=models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    name=models.CharField(max_length=150,blank=False)
    game_type = models.CharField(max_length=50)
    location=models.TextField(blank=False)
    location_url=models.TextField()
    open_time=models.TimeField()
    close_time=models.TimeField()
    rent=models.CharField(max_length=5,default=0)
    discription=models.TextField()
    slots=models.BooleanField(default=True)
    closed = models.BooleanField(default=True) 
    def __str__(self):
        return self.name
    

class reviewtable(models.Model):
    turf=models.ForeignKey(turf_table,on_delete=models.CASCADE,null=True)
    name=models.CharField(max_length=20)
    email=models.CharField(max_length=50)
    message=models.TextField()
    def __str__(self):
        return self.message


