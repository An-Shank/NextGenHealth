from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse , Http404 , HttpResponseRedirect
from .models import PHARMACY
from doctor.models import Patient,Report,MedReport
from django.template import loader , RequestContext
from django.views import View
from .forms import SubmitPID , PharLogin ,PharSignUp
from django import forms
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate , login , logout
from doctor.models import Report,Prescription
from django.contrib.auth.models import User
#from .models import PHARMACY

#def SRRes(request):
	#return HttpResponse("Invalid ID")

#	return render(request,'search.html',{} )
#def SR(request):
#	ph_id = int(request.POST['phid'])
#	result = PHARMACY.objects.filter(ph_id=ph_id)
#	if len(result)==0:
#		#return HttpResponseRedirect('/phar.html/')
#		#return HttpResponse("Invalid ID")
#		return render(request,'phar.html',{'message': "Doesn't exists"})
#	return render(request , 'phar.html' , {})

def phar_signup(request , aadharno , **kwargs) :
    form = PharSignUp()
    template = 'phar_signup.html'
    context = {'form' : form , 'message' : '' , 'aadharno' : aadharno}
    if request.POST :
        form = PharSignUp(request.POST)
        pharmacy = PHARMACY.objects.all()
        for d in pharmacy:
            print(d.user)
        phauser = request.POST.get('phauser')
        phapass = request.POST.get('phapass1')
        phamail = request.POST.get('phamail')
        u = User.objects.create_user(username = phauser , password = phapass , email = phamail)
        d = PHARMACY()
        d.ph_id = aadharno
        d.user = u
        d.ph_name = request.POST.get('phaname')
        d.ph_addr = request.POST.get('phaaddr')
        d.ph_phone = request.POST.get('phaphone')
        d.save()
        return HttpResponseRedirect(reverse('phar_index'))
    return render(request , template , context)





def login_pharuser(request) :
    form = PharLogin()
    ds = PHARMACY.objects.all()

    if request.user.is_authenticated() :
        uname = request.user.username
        for d in ds :
            if str(d.user) == uname :
                break
        out = d.ph_id
        return HttpResponseRedirect(reverse('pharpatient_index' , args=[out]))
    username = password = ""
    success = 0
    template = 'phar_user.html'
    context = {'form' : form , 'title' : "Pharmacy Login" , 'message' : ''}
    if request.POST :
        username = request.POST.get('username')
        password = request.POST.get('password')
        aadharno = request.POST.get('aadharno')
        if aadharno is not None :
            return HttpResponseRedirect(reverse('phar_reg' , args=[aadharno]))
        else:
            user = authenticate(username = username , password = password)
            if user is not None :
                if user.is_active :
                     for d in ds :
                         if str(d.user) == username :
                              success = 1
                              break
                     if success == 1 :
                         login(request , user)
                         out = d.ph_id
                         return HttpResponseRedirect(reverse('pharpatient_index' , args=[out]))
                     else :
                       context.update({'message' : 'User not Permitted'})
                else :
                 context.update({'message' : 'User is disabled'})
            else :
             context.update({'message' : 'Invalid User'})
    return render(request , template , context)



@login_required(login_url = '/pharmacy/')
def pharpatient_view(request , **kwargs) :
    form = SubmitPID()
    template = 'phar_form.html'
    report = Report.objects.all()
    pharmacy = PHARMACY.objects.all()
    context = {'form' : form , 'title' : 'Patient Report' , 'doc' : pharmacy , 'did' : kwargs['ph_id'],'rep' : reversed(report) }
    if request.POST :
        form = SubmitPID(request.POST)
        report = Report.objects.all()
        mreport = MedReport.objects.all()
        ph_id = kwargs['ph_id']
        if form.is_valid() :
            out = form.cleaned_data['pid']
            return HttpResponseRedirect(reverse('pharpatient_info' , kwargs={'patient_id' : out , 'ph_id' : ph_id}))
    return render(request , template , context)



@login_required(login_url = '/pharmacy/')
def infos(request , patient_id , ph_id, **kwargs) :
    reports = Report.objects.all()
    mreports = MedReport.objects.all()
    p_info = Patient.objects.all()
    result = Prescription.objects.all()
    phar = PHARMACY.objects.all()
    template = loader.get_template('infos.html')
    context = {'reports' : reversed(reports) , 'patient_id' : patient_id ,'ph_id' : ph_id , 'mreports' : mreports , 'p_info' : p_info,'result':result , 'phar' : phar}
    try:
        pid = Report.objects.filter(patient_no=patient_id)
    except Report.DoesNotExist:
        raise Http404("Patient record does not exist in the database")
    return HttpResponse(template.render(context , request))





#def searchResult(request):
#	pat_no = int(request.POST['pid'])
#	result = Prescription.objects.filter(pat_no=pat_no)
#	if len(result)==0:
#		return render(request,'page.html',{ 'message': "Doesn't exists" } )
	#print result.quantity
#	data = []
#	for e in result:
#		data.append(
#		{
#		'qty' : e.quantity,
#		'days' : e.days,
#		'per_day' : e.per_day,
		#'details' : result.med_id
#		})
	#print data
#	return render(request,'result.html',{ 'data': data} )

#def search(request):
	# ph_id = int(request.POST['phid'])
	# result = PHARMACY.objects.filter(ph_id=ph_id)
	# if len(result)==0:
	# 	#return HttpResponseRedirect('/phar.html/')
	# 	#return HttpResponse("Invalid ID")
	# 	return render(request,'phar.html',{'message': "Doesn't exists"})
#	return render(request,'page.html',{})
def pharreport_view(request , **kwargs) :
    form = AddReport()
    template = 'rep_form.html'
    meds = MedReport.objects.all()
    context = {'form' : form , 'title' : 'MED' , 'meds' : meds}
    if request.POST :
        form = AddReport(request.POST)
        docs = PHARMACY.objects.all()
        p_id = ord(kwargs['patient_id']) - 48
        d_id = ord(kwargs['ph_id']) - 48
        d_name = ""
        for d in docs :
            if d_id == d.ph_id :
                d_name = d.ph_name
        p = Patient.objects.get(pk=ph_id)
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
            return HttpResponseRedirect(reverse('pharpatient_info' , kwargs={'patient_id' : p_id , 'ph_id' : ph_id}))
    return render(request , template , context)
