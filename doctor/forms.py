from django import forms
from .models import Report
from django.shortcuts import render
from django.http import HttpResponseRedirect , HttpResponse
from django.urls import reverse

class SubmitPID(forms.Form) :
    pid = forms.IntegerField(label = "Patient ID")

    def clean(self) :
        cleaned_data = super(SubmitPID , self).clean()
        out = cleaned_data['pid']
        reports = Report.objects.all()
        valid = False
        for r in reports :
            if r.patient_no == out :
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
