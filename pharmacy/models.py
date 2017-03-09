from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
# Create your models here.



class PHARMACY(models.Model) :
    ph_id = models.BigIntegerField(null=False,primary_key=True)
    ph_name = models.CharField(max_length = 50)
   # ph_sx = models.CharField(max_length = 10)
    ph_addr = models.CharField(default='Nil',max_length = 100)
    ph_phone = models.BigIntegerField()
    user = models.OneToOneField(User , on_delete = models.CASCADE)

    def __str__(self):
		return self.ph_name
