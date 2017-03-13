from django.shortcuts import render
from django.http import HttpResponse , Http404 , HttpResponseRedirect
from .models import Report , MedReport , Patient , Doctor , Prescription
from django.template import loader , RequestContext
from django.views import View
from .forms import SubmitPID , DocLogin , AddReport
from django import forms
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate , login , logout
from graphos.sources.model import ModelDataSource
from graphos.sources.simple import SimpleDataSource
from graphos.renderers.yui import LineChart
# from dal import autocomplete

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

# @login_required(login_url='/doctor/')
# def logout_user(request) :
#     logout(request)
#     form = DocLogin()
#     ds = Doctor.objects.all()
#     username = password = ""
#     success = 0
#     template = 'doc_user.html'
#     context = {'form' : form , 'title' : "Doctor Login" , 'message' : ''}
#     if request.POST :
#         username = request.POST.get('username')
#         password = request.POST.get('password')
#         user = authenticate(username = username , password = password)
#         if user is not None :
#             if user.is_active :
#                 for d in ds :
#                     if str(d.user) == username :
#                         success = 1
#                         break
#                 if success == 1 :
#                     login(request , user)
#                     out = d.doc_id
#                     return HttpResponseRedirect(reverse('patient_index' , args=[out]))
#                 else :
#                     context.update({'message' : 'User not Permitted'})
#             else :
#                 context.update({'message' : 'User is disabled'})
#         else :
#             context.update({'message' : 'Invalid User'})
#     else :
#         context.update({'message' : 'User Logged Out'})
#     return render(request , template , context)

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

# class IDView(View) :
#     def get(self , request , *args , **kwargs) :
#         the_form = SubmitPID()
#         template = loader.get_template('doc_form.html')
#         context = {'form' : the_form , 'title' : "Patient Report"}
#         return HttpResponse(template.render(context , request))
#
#     def post(self , request , *args , **kwargs) :
#         form = SubmitPID(request.POST)
#         report = Report.objects.all()
#         mreport = MedReport.objects.all()
#         template = 'doc_form.html'
#         doc_id = kwargs['doc_id']
#         if form.is_valid() :
#             out = form.cleaned_data['pid']
#         #     reports = Report.objects.all()
#         #     valid = False
#         #     for r in reports :
#         #         if r.patient_no == out :
#         #             valid = True
#         #             break
#         #     if valid == False :
#         #          raise forms.ValidationError("This ID does not exist")
#         #         # SubmitPID.validate_pid(self , request , out)
#         #         # SubmitPID.clean_pid(self , request)
#         #     # for r in report :
#         #     #     print (r.date)
#         # #    return render(request , 'info.html' , {'patient_id' : out , 'reports' : report , 'mreports' : mreport})
#             return HttpResponseRedirect(reverse('patient_info' , kwargs={'patient_id' : out , 'doc_id' : doc_id}))
#         # return HttpResponse(template.render(context , request))
#         # return HttpResponseRedirect('.')
#         context = {'form' : form , 'title' : "Patient Report"}
#         return render(request , template , context)

# class DocView(View) :
#     def get(self , request , *args , **kwargs) :
#         the_form = DocLogin()
#         template = loader.get_template('doc_user.html')
#         context = {'form' : the_form , 'title' : "Doctor Login"}
#         return HttpResponse(template.render(context , request))
#
#     def post(self , request , *args , **kwargs) :
#         form = DocLogin(request.POST)
#         docs = Doctor.objects.all()
#         template = 'doc_user.html'
#         if form.is_valid() :
#             out = form.cleaned_data['username']
#             return HttpResponseRedirect(reverse('patient_index' , args=[out]))
#         context = {'form' : form , 'title' : "Doctor Login"}
#         return render(request , template , context)

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
                # if out_m:
                #     pr.morn = True
                # else :
                #     pr.morn = False
                # if out_n:
                #     pr.noon = True
                # else :
                #     pr.noon = False
                # if out_ni:
                #     pr.nite = True
                # else :
                #     pr.nite = False
                # out_m = form.process()
                # out_n = form.cleaned_data['midday']
                # out_ni = form.cleaned_data['night']
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

# class RepView(View) :
#     def get(self , request , *args , **kwargs) :
#         the_form = AddReport()
#         template = loader.get_template('rep_form.html')
#         context = {'form' : the_form , 'title' : "Add Report"}
#         return HttpResponse(template.render(context , request))
#
#     def post(self , request , *args , **kwargs) :
#         form = AddReport(request.POST)
#         docs = Doctor.objects.all()
#         p_id = ord(kwargs['patient_id']) - 48
#         d_id = ord(kwargs['doc_id']) - 48
#         d_name = ""
#         for d in docs :
#             if d_id == d.doc_id :
#                 d_name = d.doc_name
#         p = Patient.objects.get(pk=p_id)
#         template = 'rep_form.html'
#         if form.is_valid() :
#             out_med = form.cleaned_data['premeds']
#             out_note = form.cleaned_data['notes']
#             r = Report()
#             r.med = out_med
#             r.patient_no = p
#             r.notes = out_note
#             r.doc = d_name
#             r.save()
#             return HttpResponseRedirect(reverse('patient_info' , kwargs={'patient_id' : p_id , 'doc_id' : d_id}))
#         context = {'form' : form , 'title' : "Doctor Login"}
#         return render(request , template , context)
