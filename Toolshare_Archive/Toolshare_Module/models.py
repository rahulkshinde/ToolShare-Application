from django.db import models

# Create your models here.
#Class created by rahul and rohan 
class Tools(models.Model):

    name = models.CharField(max_length=50)

    toolID = models.IntegerField()

    image = models.ImageField(upload_to=None, height_field=None, width_field=None, max_length=100)

    userID = models.CharField(max_length=50)

    Description = models.CharField(max_length=50)

    uniqueness = models.CharField(max_length=100)

    avialability = models.BooleanField()

    sharingLoc = models.CharField(max_length=50)

    shedID = models.IntegerField()

    status = models.BooleanField()

    registrationDate = models.DateTimeField()

    useCount = models.IntegerField()

    lastBorrowDate = models.DateTimeField()
    