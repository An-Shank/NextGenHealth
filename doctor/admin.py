from django.contrib import admin
from .models import Report , MedReport , Patient , Doctor , Prescription
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

# class DoctorInline(admin.StackedInline):
#     model = Doctor
#     can_delete = False
#     verbose_name_plural = 'doctor'
#
# class UserAdmin(BaseUserAdmin):
#     inlines = (DoctorInline, )
#
# # Register your models here.
# admin.site.unregister(User)
# admin.site.register(User, UserAdmin)
admin.site.register(Doctor)
admin.site.register(Patient)
admin.site.register(Report)
admin.site.register(MedReport)
admin.site.register(Prescription)
