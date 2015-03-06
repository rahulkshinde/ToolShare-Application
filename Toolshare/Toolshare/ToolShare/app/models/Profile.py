#"""
#Name: Profile
#Description: This file creates models for handling user profiles.
#"""
from app.models.Sharezone import Sharezone
from django.contrib.auth.models import User
from django.db import models
# Create your models here.
from datetime import datetime
class Profile(User): #creates table for user
    user = models.OneToOneField(User)
    Middle_Name = models.CharField(max_length=30,null=True)
    Gender = models.CharField(max_length=30)
    Address1 = models.CharField(max_length=30)
    Address2 = models.CharField(max_length=30,null=True)
    PickUpArrangement = models.CharField(max_length=30)
    PhoneNumber = models.IntegerField(default=0)
    sharezone = models.ForeignKey(Sharezone,null=True) 
    BorrowCount =  models.IntegerField(default=0) #For determining the stastics of tools and user
    LendCount = models.IntegerField(default=0) #For determining the stastics of tools and user
    Dateofbirth = models.DateField(default=datetime.now())
    RemainderType = models.CharField(max_length=30,null=True) # The remainder type for use like phone or email
    RemainderFrequency=models.CharField(max_length=30,null=True) # number of times remainder sent to user
    class Meta:
        app_label = 'app'
       