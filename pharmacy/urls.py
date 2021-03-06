from django.conf.urls import url
from . import views
from django.contrib.auth.views import logout
urlpatterns = [
   # url(r'^search/' , views.search) ,
    #url(r'^search-result/' , views.searchResult) ,
    url(r'^$' , views.login_pharuser , name='pharmacy_index') ,
    url(r'^SignUp/(?P<aadharno>[0-9]+)/$' , views.phar_signup , name='phar_reg') ,
    url(r'^ph_id=(?P<ph_id>[0-9]+)/$' , views.pharpatient_view , name='pharpatient_index') ,
   # url(r'^ph_id=(?P<ph_id>[0-9]+)/patient_id=(?P<patient_id>[0-9]+)/$' , views.searchResult , name = 'patient_info'),
    url(r'^ph_id=(?P<ph_id>[0-9]+)/patient_id=(?P<patient_id>[0-9]+)/$' , views.infos , name = 'pharpatient_info') ,
   # url(r'^ph_id=(?P<ph_id>[0-9]+)/med/med_id=(?P<med_id>[0-9]+)/$' , views.med_info , name = 'med_info') ,
    url(r'^ph_id=(?P<ph_id>[0-9]+)/patient_id=(?P<patient_id>[0-9]+)/add_report/$' , views.pharreport_view ,) ,
    url(r'^logout/$' , logout , {'next_page' : '/pharmacy'} , name='pharmacy_out') ,
    # url(r'^search/' , views.SRRes) ,
   # url(r'^phar/' , views.SR) ,
    # url(r'^autocomplete/$' , views.MedicineAutoComplete.as_view() , name='autocomplete'),
]
