from django.shortcuts import render
from django.http import HttpResponse
from django.http import Http404
from .models import Report , MedReport
from django.template import loader
# Create your views here.

def index(request) :
    reports = Report.objects.all()
    template = loader.get_template('doctor/index.html')
    context = {'reports' : reports}
    ''' html = ' '
    for r in reports :
        url = '/doctor/' + str(r.patient_no) + '/'
        html += '<a href = "'+ url + '">' + str(r.patient_no) + '</a><br>' '''
    return HttpResponse(template.render(context , request))

def info(request , patient_id) :
    reports = Report.objects.all()
    mreports = MedReport.objects.all()
    template = loader.get_template('doctor/info.html')
    context = {'reports' : reports , 'patient_id' : patient_id , 'mreports' : mreports }
    try:
        pid = Report.objects.get(pk=patient_id)
    except Report.DoesNotExist:
        raise Http404("Patient record does not exist in the database")
    '''for r in reports :
        if patient_id == str(r.patient_no) :
            return HttpResponse('<h1>This contains info on patient no : ' + patient_id + '</h1>'
            '<td>Table</td>'
            '<tr>Patient No:' + str(r.patient_no) + '</tr>') '''
    return HttpResponse(template.render(context , request))

def med_info(request , med_id) :
    mreports = MedReport.objects.all()
    template = loader.get_template('doctor/med_info.html')
    context = {'mreports' : mreports , 'med_id' : med_id}
    try:
        mid = MedReport.objects.get(pk=med_id)
    except MedReport.DoesNotExist:
       raise Http404("Medicine record does not exist in the database")
    return HttpResponse(template.render(context , request))
