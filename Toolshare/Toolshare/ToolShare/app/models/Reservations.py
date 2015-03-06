#"""
#Name: Tools
#Description: This file creates models for handling tool reservations.
#"""
from app.models.Profile import Profile
from app.models.Tools import Tools
from django.db import models
# Create your models here.
from datetime import datetime
class Reservations(models.Model):
    ToolId=models.ForeignKey(Tools,null=True)
    BoorowerId=models.ForeignKey(Profile,null=True)
    Owner= models.CharField(max_length=30,null=True)
    StartDate = models.DateTimeField()
    EndDate = models.DateTimeField()
    status= models.CharField(max_length=30,null=True)
    class Meta:
        app_label = 'app'