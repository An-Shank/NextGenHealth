from django.conf.urls import url
from . import views
from django.contrib.auth.views import logout
#from .models import Report

urlpatterns = [
    url(r'^$' , views.login_patuser , name='patient_index') ,
    url(r'^pat_id=(?P<patient_id>[0-9]+)/$' , views.pat_info , name='patient_info') ,
    # url(r'^doc_id=(?P<doc_id>[0-9]+)/med/med_id=(?P<med_id>[0-9]+)/$' , views.med_info , name = 'med_info') ,
    # url(r'^doc_id=(?P<doc_id>[0-9]+)/patient_id=(?P<patient_id>[0-9]+)/add_report/$' , views.report_view , name = 'add_report') ,
    url(r'^logout/$' , logout , {'next_page' : '/patient'} , name='patient_out') ,
]
