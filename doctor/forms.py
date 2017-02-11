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

class AddReport(forms.Form) :
    premeds = forms.CharField(label = 'Meds')
    notes = forms.CharField(label = 'Notes')
    def clean(self) :
        cleaned_data = super(AddReport , self).clean()
        out_med = cleaned_data['premeds']
        out_note = cleaned_data['notes']
