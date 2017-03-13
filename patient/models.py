from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Patient(models.Model) :
    p_id = models.BigIntegerField(primary_key=True)
    user = models.OneToOneField(User , on_delete = models.CASCADE)
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
