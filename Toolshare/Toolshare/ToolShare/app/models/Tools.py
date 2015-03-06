#"""
#Name: Tools
#Description: This file creates models for handling tools.
#"""
from app.models.Profile import Profile
from app.models.Shed import Shed
from django.db import models
# Create your models here.
from datetime import datetime
from django.db.models.signals import post_delete
from django.dispatch import receiver
class Tools(models.Model):
    name = models.CharField(max_length=50)
    userID=models.ForeignKey(Profile,null=True)
    Description = models.CharField(max_length=50)
    Category = models.CharField(max_length=30)
    uniqueness = models.CharField(max_length=100)
    availability = models.BooleanField()
    pickuparrangement = models.CharField(max_length=50)
    shedID = models.ForeignKey(Shed,null=True,blank=True)
    status = models.CharField(max_length=30)
    registrationDate = models.DateTimeField()
    useCount = models.IntegerField()
    lastBorrowDate = models.DateTimeField()
    activation=models.BooleanField()
    Address1 = models.CharField(max_length=30,null=True,blank=True)
    Address2 = models.CharField(max_length=30,null=True,blank=True)
    stuff_image = models.ImageField(upload_to="img/")
    class Meta:
        app_label = 'app'