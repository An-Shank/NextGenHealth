from django import forms
from .models import Report , Doctor , Patient
from django.shortcuts import render
from django.http import HttpResponseRedirect , HttpResponse
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.exceptions import NON_FIELD_ERRORS

class SubmitPID(forms.Form) :
    pid = forms.IntegerField(label="" , widget = forms.TextInput(attrs={'class' : 'form-control' , 'placeholder' : 'Patient ID'}))

    def clean(self) :
        cleaned_data = super(SubmitPID , self).clean()
        out = cleaned_data['pid']
        reports = Patient.objects.all()
        valid = False
        for r in reports :
            if r.p_id == out :
                valid = True
                break
        if valid == False :
            raise forms.ValidationError('This ID does not exist')

class DocLogin(forms.Form) :
    username = forms.CharField(label = "" , widget = forms.TextInput(attrs={'class' : 'form-control' , 'placeholder' : 'Username'}))
    password = forms.CharField(label = 'Password' , max_length = 50 , widget = forms.PasswordInput(attrs={'class' : 'form-control' , 'placeholder' : 'Password'}))
    aadharno = forms.CharField(label = "" , widget = forms.TextInput(attrs={'class' : 'form-control' , 'placeholder' : 'Aadhar No'}))

def calculate_days() :
    out = []
    for i in range(1,31) :
        out.append((i , i))
    return out
def calculate_dose() :
    vals = [0.25 , 0.5 , 0.75 , 1 , 2 , 3]
    out = []
    for v in vals :
        out.append((v , v))
    return out
class AddReport(forms.Form) :
    premeds = forms.CharField(label = 'Meds' , widget = forms.TextInput(attrs={'class' : 'form-control' , 'placeholder' : 'Presciption' , 'list' : 'medlist'}))
    # notes = forms.CharField(label = 'Notes' , widget = forms.TextInput(attrs={'class' : 'form-control' , 'placeholder' : 'Notes'}))
    morning = forms.ChoiceField(choices = [(0 , 'No') , (1 , 'Yes')] , widget = forms.Select(attrs={'class' : 'form-control'}))
    midday = forms.ChoiceField(choices = [(0 , 'No') , (1 , 'Yes')] , widget = forms.Select(attrs={'class' : 'form-control'}))
    night = forms.ChoiceField(choices = [(0 , 'No') , (1 , 'Yes')] , widget = forms.Select(attrs={'class' : 'form-control'}))
    # midday = forms.BooleanField(label = 'Noon' , required=False , initial=False)
    # night = forms.BooleanField(label = 'Night' , required=False , initial=False)
    befter = forms.ChoiceField(choices = [('Before' , 'Before') , ('After' , 'After')] , widget = forms.Select(attrs={'class' : 'form-control'}))
    # dose = forms.DecimalField(label="" , widget = forms.TextInput(attrs={'class' : 'form-control' , 'placeholder' : 'Dose'}) , decimal_places = 2)
    dose = forms.ChoiceField(choices = calculate_dose() , widget = forms.Select(attrs={'class' : 'form-control'}))
    # day = forms.IntegerField(label="" , widget = forms.TextInput(attrs={'class' : 'form-control' , 'placeholder' : 'Days'}))
    day = forms.ChoiceField(choices = calculate_days() , widget = forms.Select(attrs={'class' : 'form-control'}))
    attach = forms.ImageField(required = False)

class DocSignUp(forms.Form) :
    duser = forms.CharField(label = "" , widget = forms.TextInput(attrs={'class' : 'form-control' , 'placeholder' : 'Username'}))
    dpass1 = forms.CharField(label = 'Password' , max_length = 50 , widget = forms.PasswordInput(attrs={'class' : 'form-control' , 'placeholder' : 'Password'}))
    dpass2 = forms.CharField(label = 'Password' , max_length = 50 , widget = forms.PasswordInput(attrs={'class' : 'form-control' , 'placeholder' : 'Password'}))
    aadharno = forms.CharField(label = "" , widget = forms.TextInput(attrs={'class' : 'form-control' , 'placeholder' : 'Aadhar No'}))
    dmail = forms.CharField(label = "" , widget = forms.TextInput(attrs={'class' : 'form-control' , 'placeholder' : 'Email'}))
    dname = forms.CharField(label = "" , widget = forms.TextInput(attrs={'class' : 'form-control' , 'placeholder' : 'Name'}))
    dimage = forms.ImageField(required = True)
    dsx = forms.CharField(label = "" , widget = forms.TextInput(attrs={'class' : 'form-control' , 'placeholder' : 'Sex'}))
    daddr = forms.CharField(label = "" , widget = forms.TextInput(attrs={'class' : 'form-control' , 'placeholder' : 'Address'}))
    dphone = forms.CharField(label = "" , widget = forms.TextInput(attrs={'class' : 'form-control' , 'placeholder' : 'Contact No'}))
