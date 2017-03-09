from django.conf.urls import url
from . import views
#from .models import Report
from django.contrib.auth.views import logout
urlpatterns = [
   # url(r'^search/' , views.search) ,
    #url(r'^search-result/' , views.searchResult) ,
    url(r'^$' , views.login_user , name='pharmacy_index') ,
    url(r'^ph_id=(?P<ph_id>[0-9]+)/$' , views.patient_view , name='patient_index') ,
   # url(r'^ph_id=(?P<ph_id>[0-9]+)/patient_id=(?P<patient_id>[0-9]+)/$' , views.searchResult , name = 'patient_info'),
    url(r'^ph_id=(?P<ph_id>[0-9]+)/patient_id=(?P<patient_id>[0-9]+)/$' , views.infos , name = 'patient_info') ,
   # url(r'^ph_id=(?P<ph_id>[0-9]+)/med/med_id=(?P<med_id>[0-9]+)/$' , views.med_info , name = 'med_info') ,
    url(r'^ph_id=(?P<ph_id>[0-9]+)/patient_id=(?P<patient_id>[0-9]+)/add_report/$' , views.report_view ,) ,
    url(r'^logout/$' , logout , {'next_page' : '/pharmacy'} , name='pharmacy_out') ,
    # url(r'^search/' , views.SRRes) ,
   # url(r'^phar/' , views.SR) ,
    # url(r'^autocomplete/$' , views.MedicineAutoComplete.as_view() , name='autocomplete'),
]
