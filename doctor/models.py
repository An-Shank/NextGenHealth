from django.db import models
from time import strftime
from django.contrib.auth.models import User

# Create your models here.

class Doctor(models.Model) :
    doc_id = models.BigIntegerField(primary_key=True)
    user = models.OneToOneField(User , on_delete = models.CASCADE)
    doc_image = models.ImageField(upload_to = 'images/doctors')
    doc_name = models.CharField(max_length = 50)
    doc_sx = models.CharField(max_length = 10)
    doc_addr = models.CharField(max_length = 100)
    doc_phone = models.BigIntegerField()
    def __str__(self) :
        return self.doc_name

class Patient(models.Model) :
    p_id = models.BigIntegerField(primary_key=True)
    p_image = models.ImageField(upload_to = 'images/patients')
    p_name = models.CharField(max_length = 50)
    p_age = models.IntegerField(null=False)
    p_sx = models.CharField(max_length = 10)
    p_addr = models.CharField(max_length = 100)
    p_NoK = models.CharField(max_length = 50 , default = "Nil")
    p_blood = models.CharField(max_length = 3)
    p_contact = models.CharField(max_length = 50)
    p_allerg = models.CharField(max_length = 100 , default = "Nil")

    def __str__(self) :
        return self.p_name

    def returnpid(self) :
        return self.p_id

class Report(models.Model) :
    patient_no = models.ForeignKey(Patient)
    date = models.DateTimeField(auto_now_add = True)
    med = models.CharField(max_length = 1000)
    attach = models.ImageField(upload_to = 'images/attachments' , null = True , blank = True)
    doc = models.CharField(max_length = 50)

    class Meta :
        unique_together = (('patient_no' , 'date'),)

    @property
    def medsplit(self) :
        return self.med.split(',')
    @property
    def imgsplit(self) :
        return str(self.attach).split('/')[2][0:10]

    def __str__(self) :
        return str(self.date)

class MedReport(models.Model) :
    med_no = models.BigIntegerField(primary_key=True)
    medname = models.CharField(max_length = 50)
    gname = models.CharField(max_length = 100)
    details = models.CharField(max_length = 1000)
    side_effect = models.CharField(max_length = 1000)

    def __str__(self) :
        return self.medname

class Prescription(models.Model) :
    pres_id = models.ForeignKey(Report)
    dosage = models.DecimalField(max_digits = 3 , decimal_places = 2 , default = 1)
    morn = models.BooleanField()
    noon = models.BooleanField()
    nite = models.BooleanField()
    timing = models.CharField(max_length = 10)
    days = models.IntegerField(default = 1)

    def __str__(self) :
         return str(self.pres_id)
