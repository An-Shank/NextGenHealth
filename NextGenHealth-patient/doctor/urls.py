from django.conf.urls import url,include
from . import views
#from .models import Report

urlpatterns = [
    url(r'^$' , views.index , name = 'index') ,
    url(r'^(?P<patient_id>[0-9]+)/$' , views.info , name = 'info') ,
    #url(r'^med/(?P<med_id>[0-9]+)/$' , views.med_info , name = 'med_info') ,
    url(r'^med/(?P<med_id>[0-9]+)/$' , views.med_info , name = 'med_info'),
    
]
