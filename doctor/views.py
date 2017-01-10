from django.shortcuts import render
from django.http import HttpResponse , Http404 , HttpResponseRedirect
from .models import Report , MedReport
from django.template import loader , RequestContext
from django.views import View
from .forms import SubmitPID
from django import forms
from django.urls import reverse

# Create your views here.
'''def index(request) :
    reports = Report.objects.all()
    template = loader.get_template('doc_form.html')
    context = {'reports' : reports}
    return HttpResponse(template.render(context , request))'''
class IDView(View) :
    def get(self , request , *args , **kwargs) :
        the_form = SubmitPID()
        #reports = Report.objects.all()
        template = loader.get_template('doc_form.html')
        context = {'form' : the_form , 'title' : "Patient Report"}
        return HttpResponse(template.render(context , request))

    def post(self , request , *args , **kwargs) :
        form = SubmitPID(request.POST)
        report = Report.objects.all()
        mreport = MedReport.objects.all()
        template = loader.get_template('doc_form.html')
        context = {'form' : form , 'title' : "Patient Report"}
        if form.is_valid() :
            out = form.cleaned_data['pid']
            reports = Report.objects.all()
            valid = False
            for r in reports :
                if r.patient_no == out :
                    valid = True
                    break
            if valid == False :
                raise forms.ValidationError("This ID does not exist")
            for r in report :
                print (r.date)
        #    return render(request , 'info.html' , {'patient_id' : out , 'reports' : report , 'mreports' : mreport})
        return HttpResponseRedirect(reverse('info' , args=[out]))
        return HttpResponse(template.render(context , request))

def info(request , patient_id) :
    reports = Report.objects.all()
    mreports = MedReport.objects.all()
    template = loader.get_template('info.html')
    context = {'reports' : reports , 'patient_id' : patient_id , 'mreports' : mreports }
    try:
        pid = Report.objects.get(pk=patient_id)
    except Report.DoesNotExist:
        raise Http404("Patient record does not exist in the database")
    return HttpResponse(template.render(context , request))

def med_info(request , med_id) :
    mreports = MedReport.objects.all()
    template = loader.get_template('med_info.html')
    context = {'mreports' : mreports , 'med_id' : med_id}
    try:
        mid = MedReport.objects.get(pk=med_id)
    except MedReport.DoesNotExist:
       raise Http404("Medicine record does not exist in the database")
    return HttpResponse(template.render(context , request))
