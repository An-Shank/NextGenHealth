from __future__ import unicode_literals

from django.db import models

# Create your models here.
class PatientInfo(models.Model):
    #Basic Info
    firstname=models.CharField(max_length=25)
    lastname=models.CharField(max_length=25)
    #dob=models.CharField(max_length=10)
    age=models.DecimalField(max_digits=3,decimal_places=0)
    sex=models.CharField(max_length=1)
    bloodgroup=models.CharField(max_length=3)
    mobile=models.DecimalField(max_digits=10,decimal_places=0)
    #Address
    house=models.CharField(max_length=25)
    street=models.CharField(max_length=50)
    locality=models.CharField(max_length=25)
    city=models.CharField(max_length=25)
    state=models.CharField(max_length=25)
