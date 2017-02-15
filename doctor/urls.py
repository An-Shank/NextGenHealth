from django.conf.urls import url
from . import views
from django.contrib.auth.views import login
#from .models import Report

urlpatterns = [
    url(r'^$' , views.DocView.as_view() , name='doctor_index') ,
    url(r'^login/' , login , {'template_name' : 'doc_user.html'}) ,
    url(r'^doc_id=(?P<doc_id>[0-9]+)/$' , views.IDView.as_view() , name='patient_index') ,
    url(r'^doc_id=(?P<doc_id>[0-9]+)/patient_id=(?P<patient_id>[0-9]+)/$' , views.info , name = 'patient_info') ,
    url(r'^doc_id=(?P<doc_id>[0-9]+)/med/med_id=(?P<med_id>[0-9]+)/$' , views.med_info , name = 'med_info') ,
    url(r'^doc_id=(?P<doc_id>[0-9]+)/patient_id=(?P<patient_id>[0-9]+)/add_report/$' , views.RepView.as_view() , name = 'add_report') ,
]
