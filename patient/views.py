from django.shortcuts import render
from django.http import HttpResponse , Http404 , HttpResponseRedirect
from doctor.models import Report , MedReport , Doctor , Prescription
from .models import Patient
from django.template import loader , RequestContext
from django.views import View
from django import forms
from .forms import PatLogin
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate , login , logout
# Create your views here.

def login_patuser(request) :
    form = PatLogin()
    ps = Patient.objects.all()
    if request.user.is_authenticated() :
        uname = request.user.username
        for p in ps :
            if str(p.user) == uname :
                break
        out = p.p_id
        return HttpResponseRedirect(reverse('patient_info' , args=[out]))
    username = password = ""
    success = 0
    template = 'pat_user.html'
    context = {'form' : form , 'title' : "Patient Login" , 'message' : ''}
    if request.POST :
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username = username , password = password)
        if user is not None :
            if user.is_active :
                for p in ps :
                    if str(p.user) == username :
                        success = 1
                        break
                if success == 1 :
                    login(request , user)
                    out = p.p_id
                    return HttpResponseRedirect(reverse('patient_info' , args=[out]))
                else :
                    context.update({'message' : 'User not Permitted'})
            else :
                context.update({'message' : 'User is disabled'})
        else :
            context.update({'message' : 'Invalid User'})
    return render(request , template , context)

@login_required(login_url = '/patient/')
def pat_info(request , patient_id , **kwargs) :
    reports = Report.objects.all()
    mreports = MedReport.objects.all()
    p_info = Patient.objects.all()
    pres_info = Prescription.objects.all()
    template = loader.get_template('pat_info.html')
    context = {'reports' : reversed(reports) , 'patient_id' : patient_id , 'mreports' : mreports , 'p_info' : p_info , 'pres_info' : pres_info}
    try:
        pid = Report.objects.filter(patient_no=patient_id)
    except Report.DoesNotExist:
        raise Http404("Patient record does not exist in the database")
    return HttpResponse(template.render(context , request))
