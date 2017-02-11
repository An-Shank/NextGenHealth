from django import forms
from .models import Report , Doctor
from django.shortcuts import render
from django.http import HttpResponseRedirect , HttpResponse
from django.urls import reverse
from django.contrib.auth.models import User

class SubmitPID(forms.Form) :
    pid = forms.IntegerField(label = "Patient ID")

    def clean(self) :
        cleaned_data = super(SubmitPID , self).clean()
        out = cleaned_data['pid']
        reports = Report.objects.all()
        valid = False
        for r in reports :
            if r.patient_no.p_id == out :
                valid = True
                break
        if valid == False :
            raise forms.ValidationError('This ID does not exist')

    # def clean_pid(self, request) :
    #     out = self.cleaned_data['pid']
    #     reports = Report.objects.all()
    #     valid = False
    #     for r in reports :
    #         if r.patient_no == out :
    #             valid = True
    #             break
    #     if valid == False :
    #         raise forms.ValidationError("This ID does not exist")
    #     return out
    #
    # def validate_pid(self , request , out) :
    #     # out = self.cleaned_data['pid']
    #     reports = Report.objects.all()
    #     valid = False
    #     for r in reports :
    #         if r.patient_no == out :
    #             valid = True
    #             break
    #     if valid == False :
    #         print("Working")
    #         raise forms.ValidationError("This ID does not exist")
    #     return out
class DocLogin(forms.Form) :
    did = forms.IntegerField(label = 'Doctor ID')
    password = forms.CharField(label = 'Password' , max_length = 50 , widget = forms.PasswordInput)

    def clean(self) :
        cleaned_data = super(DocLogin , self).clean()
        out_id = cleaned_data['did']
        out_pass = cleaned_data['password']
        docs = Doctor.objects.all()
        valid = False
        authorize = False
        for d in docs :
            if d.doc_id == out_id :
                valid = True
                if d.doc_pass == out_pass :
                    authorize = True
                break
        if valid == False :
            raise forms.ValidationError('This ID does not exist')
        elif authorize == False :
            raise forms.ValidationError('Incorrect Password')
