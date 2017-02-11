from django.contrib import admin
from .models import Report , MedReport , Patient , Doctor

# Register your models here.
admin.site.register(Doctor)
admin.site.register(Patient)
admin.site.register(Report)
admin.site.register(MedReport)
