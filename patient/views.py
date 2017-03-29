from django.shortcuts import render
from django.http import HttpResponse , Http404 , HttpResponseRedirect
from doctor.models import Report , MedReport , Doctor , Prescription
from .models import Patient
from django.template import loader , RequestContext
from django.views import View
from django import forms
from .forms import PatLogin , PatSignUp
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate , login , logout
from django.contrib.auth.models import User
# Create your views here.

def mainpage(request) :
    return render(request , 'index.html' , {})

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
        aadharno = request.POST.get('aadharno')
        if aadharno is not None :
            return HttpResponseRedirect(reverse('pat_reg' , args=[aadharno]))
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

def pat_signup(request , aadharno , **kwargs) :
    form = PatSignUp()
    template = 'pat_signup.html'
    context = {'form' : form , 'message' : '' , 'aadharno' : aadharno}
    if request.POST :
        form = PatSignUp(request.POST)
        patient = Patient.objects.all()
        puser = request.POST.get('puser')
        ppass = request.POST.get('ppass1')
        pmail = request.POST.get('pmail')
        u = User.objects.create_user(username = puser , password = ppass , email = pmail)
        p = Patient()
        p.p_id = aadharno
        p.user = u
        p.p_image = request.POST.get('pimage')
        p.p_name = request.POST.get('pname')
        p.p_age = request.POST.get('page')
        p.p_sx = request.POST.get('psx')
        p.p_addr = request.POST.get('paddr')
        p.p_contact = request.POST.get('pphone')
        p.p_NoK = request.POST.get('pnok')
        p.p_blood = request.POST.get('pblood')
        p.p_allerg = request.POST.get('pallerg')
        p.save()
        return HttpResponseRedirect(reverse('patient_index'))
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
