from django.shortcuts import render
from django.http import HttpResponse , Http404 , HttpResponseRedirect
from .models import Report , MedReport , Patient , Doctor
from django.template import loader , RequestContext
from django.views import View
from .forms import SubmitPID , DocLogin , AddReport
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
        template = loader.get_template('doc_form.html')
        context = {'form' : the_form , 'title' : "Patient Report"}
        return HttpResponse(template.render(context , request))

    def post(self , request , *args , **kwargs) :
        form = SubmitPID(request.POST)
        report = Report.objects.all()
        mreport = MedReport.objects.all()
        patients = Patient.objects.all()
        template = 'doc_form.html'
        context = {'form' : form , 'title' : "Patient Report"}
        doc_id = kwargs['doc_id']
        if form.is_valid() :
            out = form.cleaned_data['pid']
            for p in patients :
                if p.p_id == out :
        #     reports = Report.objects.all()
        #     valid = False
        #     for r in reports :
        #         if r.patient_no == out :
        #             valid = True
        #             break
        #     if valid == False :
        #          raise forms.ValidationError("This ID does not exist")
        #         # SubmitPID.validate_pid(self , request , out)
        #         # SubmitPID.clean_pid(self , request)
        #     # for r in report :
        #     #     print (r.date)
        # #    return render(request , 'info.html' , {'patient_id' : out , 'reports' : report , 'mreports' : mreport})
                    return HttpResponseRedirect(reverse('patient_info' , kwargs={'patient_id' : out , 'doc_id' : doc_id}))
        # return HttpResponse(template.render(context , request))
        # return HttpResponseRedirect('.')
        return render(request , template , context)

class DocView(View) :
    def get(self , request , *args , **kwargs) :
        the_form = DocLogin()
        template = loader.get_template('doc_user.html')
        context = {'form' : the_form , 'title' : "Doctor Login"}
        return HttpResponse(template.render(context , request))

    def post(self , request , *args , **kwargs) :
        form = DocLogin(request.POST)
        docs = Doctor.objects.all()
        template = 'doc_user.html'
        if form.is_valid() :
            out = form.cleaned_data['did']
            return HttpResponseRedirect(reverse('patient_index' , args=[out]))
        context = {'form' : form , 'title' : "Doctor Login"}
        return render(request , template , context)

def info(request , patient_id , **kwargs) :
    reports = Report.objects.all()
    mreports = MedReport.objects.all()
    p_info = Patient.objects.all()
    template = loader.get_template('info.html')
    context = {'reports' : reports , 'patient_id' : patient_id , 'mreports' : mreports , 'p_info' : p_info}
    try:
        pid = Report.objects.filter(patient_no=patient_id)
    except Report.DoesNotExist:
        raise Http404("Patient record does not exist in the database")
    return HttpResponse(template.render(context , request))

def med_info(request , med_id , **kwargs) :
    mreports = MedReport.objects.all()
    template = loader.get_template('med_info.html')
    context = {'mreports' : mreports , 'med_id' : med_id}
    try:
        mid = MedReport.objects.get(pk=med_id)
    except MedReport.DoesNotExist:
       raise Http404("Medicine record does not exist in the database")
    return HttpResponse(template.render(context , request))

class RepView(View) :
    def get(self , request , *args , **kwargs) :
        the_form = AddReport()
        template = loader.get_template('rep_form.html')
        context = {'form' : the_form , 'title' : "Add Report"}
        return HttpResponse(template.render(context , request))

    def post(self , request , *args , **kwargs) :
        form = AddReport(request.POST)
        docs = Doctor.objects.all()
        p_id = ord(kwargs['patient_id']) - 48
        d_id = ord(kwargs['doc_id']) - 48
        d_name = ""
        for d in docs :
            if d_id == d.doc_id :
                d_name = d.doc_name
        p = Patient.objects.get(pk=p_id)
        template = 'rep_form.html'
        if form.is_valid() :
            out_med = form.cleaned_data['premeds']
            out_note = form.cleaned_data['notes']
            r = Report()
            r.med = out_med
            r.patient_no = p
            r.notes = out_note
            r.doc = d_name
            r.save()
            return HttpResponseRedirect(reverse('patient_info' , kwargs={'patient_id' : p_id , 'doc_id' : d_id}))
        context = {'form' : form , 'title' : "Doctor Login"}
        return render(request , template , context)
