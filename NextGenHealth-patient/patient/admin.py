from django.contrib import admin

# Register your models here.
from .models import PatientInfo

admin.site.register(PatientInfo)
