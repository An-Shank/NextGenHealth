from django.shortcuts import render
from django.http import HttpResponse , Http404 , HttpResponseRedirect
from .models import Report , MedReport , Doctor , Prescription
from patient.models import Patient
from django.template import loader , RequestContext
from django.views import View
from .forms import SubmitPID , DocLogin , AddReport , DocSignUp
from django import forms
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate , login , logout
from django.contrib.auth.models import User

# Create your views here.

def login_user(request) :
    form = DocLogin()
    ds = Doctor.objects.all()
    if request.user.is_authenticated() :
        uname = request.user.username
        for d in ds :
            if str(d.user) == uname :
                break
        out = d.doc_id
        return HttpResponseRedirect(reverse('patient_index' , args=[out]))
    username = password = ""
    success = 0
    template = 'doc_user.html'
    context = {'form' : form , 'title' : "Doctor Login" , 'message' : ''}
    if request.POST :
        username = request.POST.get('username')
        password = request.POST.get('password')
        aadharno = request.POST.get('aadharno')
        if aadharno is not None :
            return HttpResponseRedirect(reverse('doc_reg' , args=[aadharno]))
        else :
            user = authenticate(username = username , password = password)
            if user is not None :
                if user.is_active :
                    for d in ds :
                        if str(d.user) == username :
                            success = 1
                            break
                    if success == 1 :
                        login(request , user)
                        out = d.doc_id
                        return HttpResponseRedirect(reverse('patient_index' , args=[out]))
                    else :
                        context.update({'message' : 'User not Permitted'})
                else :
                    context.update({'message' : 'User is disabled'})
            else :
                context.update({'message' : 'Invalid User'})
    return render(request , template , context)

def doc_signup(request , aadharno , **kwargs) :
    form = DocSignUp()
    template = 'doc_signup.html'
    context = {'form' : form , 'message' : '' , 'aadharno' : aadharno}
    if request.POST :
        form = DocSignUp(request.POST)
        doctor = Doctor.objects.all()
        for d in doctor :
            print(d.user)
        duser = request.POST.get('duser')
        dpass = request.POST.get('dpass1')
        dmail = request.POST.get('dmail')
        u = User.objects.create_user(username = duser , password = dpass , email = dmail)
        d = Doctor()
        d.doc_id = aadharno
        d.user = u
        d.doc_image = request.POST.get('dimage')
        d.doc_name = request.POST.get('dname')
        d.doc_sx = request.POST.get('dsx')
        d.doc_addr = request.POST.get('daddr')
        d.doc_phone = request.POST.get('dphone')
        d.save()
        return HttpResponseRedirect(reverse('doctor_index'))
    return render(request , template , context)

@login_required(login_url = '/doctor/')
def patient_view(request , **kwargs) :
    form = SubmitPID()
    template = 'doc_form.html'
    doctor = Doctor.objects.filter(doc_id=kwargs['doc_id'])
    report = Report.objects.all()
    mreports = MedReport.objects.all()
    pres_info = Prescription.objects.all()
    context = {'form' : form , 'title' : 'Patient Report' , 'doc' : doctor , 'did' : kwargs['doc_id'] , 'rep' : reversed(report) , 'mreports' : mreports , 'pres_info' : pres_info}
    if request.POST :
        form = SubmitPID(request.POST)
        report = Report.objects.all()
        mreport = MedReport.objects.all()
        doc_id = kwargs['doc_id']
        if form.is_valid() :
            out = form.cleaned_data['pid']
            return HttpResponseRedirect(reverse('patient_info' , kwargs={'patient_id' : out , 'doc_id' : doc_id}))
    return render(request , template , context)

@login_required(login_url = '/doctor/')
def info(request , patient_id , **kwargs) :
    reports = Report.objects.all()
    mreports = MedReport.objects.all()
    p_info = Patient.objects.all()
    pres_info = Prescription.objects.all()
    template = loader.get_template('info.html')
    context = {'reports' : reversed(reports) , 'patient_id' : patient_id , 'mreports' : mreports , 'p_info' : p_info , 'pres_info' : pres_info}
    try:
        pid = Report.objects.filter(patient_no=patient_id)
    except Report.DoesNotExist:
        raise Http404("Patient record does not exist in the database")
    return HttpResponse(template.render(context , request))

@login_required(login_url = '/doctor/')
def med_info(request , med_id , **kwargs) :
    mreports = MedReport.objects.all()
    template = loader.get_template('med_info.html')
    context = {'mreports' : mreports , 'med_id' : med_id}
    try:
        mid = MedReport.objects.get(pk=med_id)
    except MedReport.DoesNotExist:
       raise Http404("Medicine record does not exist in the database")
    return HttpResponse(template.render(context , request))

@login_required(login_url = '/doctor/')
def report_view(request , **kwargs) :
    form = AddReport()
    template = 'rep_form.html'
    meds = MedReport.objects.all()
    context = {'form' : form , 'title' : 'Add Report' , 'meds' : meds}
    out_med = []
    if request.POST :
        form = AddReport(request.POST)
        docs = Doctor.objects.all()
        p_id = kwargs['patient_id']
        d_id = kwargs['doc_id']
        d_name = ""
        for d in docs :
            if d_id == str(d.doc_id) :
                d_name = d.doc_name
        p = Patient.objects.get(pk=p_id)
        template = 'rep_form.html'
        if form.is_valid() :
            out_med = request.POST.getlist('premeds')
            print(request.POST)
            out_days = request.POST.getlist('day')
            out_dose = request.POST.getlist('dose')
            out_scd = request.POST.getlist('befter')
            out_m = request.POST.getlist('morning')
            out_n = request.POST.getlist('midday')
            out_ni = request.POST.getlist('night')
            r = Report()
            r.med = ','.join(o for o in out_med)
            r.patient_no = p
            r.doc = d_name
            r.save()
            count = 0
            for o in out_med :
                pr = Prescription()
                for i in meds :
                    if o == i.medname :
                        pr.med_id = i
                print(out_scd[count])
                pr.dosage = out_dose[count]
                pr.pat_no = p
                out_m = [o == 'on' for o in out_m]
                pr.morn = out_m[count]
                pr.noon = out_n[count]
                pr.nite = out_ni[count]
                pr.timing = out_scd[count]
                pr.days = out_days[count]
                pr.pres_id = r
                pr.save()
                count += 1
            return HttpResponseRedirect(reverse('patient_info' , kwargs={'patient_id' : p_id , 'doc_id' : d_id}))
    return render(request , template , context)
