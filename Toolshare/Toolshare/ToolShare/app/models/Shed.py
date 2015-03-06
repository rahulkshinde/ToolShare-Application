#"""
#Name: Shed
#Description: This file creates models for handling community shed.
#"""
from django.db import models
from app.models.Sharezone import Sharezone
from app.models.Profile import Profile
from django.contrib.auth.models import User
from datetime import datetime
class Shed(models.Model):
    Name=models.CharField(max_length=128)
    Address1=models.CharField(max_length=256)
    Address2=models.CharField(max_length=256)
    ShareZoneId=models.ForeignKey(Sharezone)
    CordinatorUserId=models.ForeignKey(Profile)
    class Meta:
        app_label = 'app'
