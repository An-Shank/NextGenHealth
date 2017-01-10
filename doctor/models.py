from django.db import models
# Create your models here.

class Report(models.Model) :
    patient_no = models.BigIntegerField(primary_key=True)
    date = models.CharField(max_length = 10)
    med = models.CharField(max_length = 1000)
    notes = models.CharField(max_length = 1000)
    doc = models.CharField(max_length = 50)

    @property
    def medsplit(self) :
        return self.med.split(',')

    def __str__(self) :
        return self.date

    def save(self , *args , **kwargs) :
        super(Report , self().save(*args , **kwargs))

class MedReport(models.Model) :
    med_no = models.BigIntegerField(primary_key=True)
    medname = models.CharField(max_length = 50)
    details = models.CharField(max_length = 1000)
    side_effect = models.CharField(max_length = 1000)

    def __str__(self) :
        return self.medname
