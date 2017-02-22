from django.conf.urls import url
from . import views
#from .models import Report

urlpatterns = [
    url(r'^$' , views.login_user , name='doctor_index') ,
    url(r'^doc_id=(?P<doc_id>[0-9]+)/$' , views.patient_view , name='patient_index') ,
    url(r'^doc_id=(?P<doc_id>[0-9]+)/patient_id=(?P<patient_id>[0-9]+)/$' , views.info , name = 'patient_info') ,
    url(r'^doc_id=(?P<doc_id>[0-9]+)/med/med_id=(?P<med_id>[0-9]+)/$' , views.med_info , name = 'med_info') ,
    url(r'^doc_id=(?P<doc_id>[0-9]+)/patient_id=(?P<patient_id>[0-9]+)/add_report/$' , views.report_view , name = 'add_report') ,
]
