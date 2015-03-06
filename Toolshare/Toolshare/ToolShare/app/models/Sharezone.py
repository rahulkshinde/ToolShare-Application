#"""
#Name: Sharezone
#Description: This file creates models for handling sharezones.
#"""
from app.models import *
from django.contrib.auth.models import User
from django.db import models
# Create your models here.
from datetime import datetime
class Sharezone(models.Model):
    SharezoneName = models.CharField(max_length=30)
    City = models.CharField(max_length=30)
    State = models.CharField(max_length=30)
    Country = models.CharField(max_length=30)
    ZipCode = models.IntegerField(primary_key=True)
    class Meta:
        app_label = 'app'

