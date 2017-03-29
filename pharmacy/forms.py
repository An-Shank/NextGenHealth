from django import forms
from .models import PHARMACY
from doctor.models import Patient
from django.shortcuts import render
from django.http import HttpResponseRedirect , HttpResponse
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.exceptions import NON_FIELD_ERRORS



class SubmitPID(forms.Form) :
    pid = forms.IntegerField(label="" , widget = forms.TextInput(attrs={'class' : 'form-control' , 'placeholder' : 'Patient ID'}))

    
class PharLogin(forms.Form) :
    username = forms.CharField(label = "" , widget = forms.TextInput(attrs={'class' : 'form-control' , 'placeholder' : 'Username'}))
    password = forms.CharField(label = 'Password' , max_length = 50 , widget = forms.PasswordInput(attrs={'class' : 'form-control' , 'placeholder' : 'Password'}))
    aadharno = forms.CharField(label = "" , widget = forms.TextInput(attrs={'class' : 'form-control' , 'placeholder' : 'Aadhar No'}))

    # def clean(self) :
    #     cleaned_data = super(DocLogin , self).clean()

class PharSignUp(forms.Form) :
    phauser = forms.CharField(label = "" , widget = forms.TextInput(attrs={'class' : 'form-control' , 'placeholder' : 'Username'}))
    phapass1 = forms.CharField(label = 'Password' , max_length = 50 , widget = forms.PasswordInput(attrs={'class' : 'form-control' , 'placeholder' : 'Password'}))
    phapass2 = forms.CharField(label = 'Password' , max_length = 50 , widget = forms.PasswordInput(attrs={'class' : 'form-control' , 'placeholder' : 'Password'}))
    aadharno = forms.CharField(label = "" , widget = forms.TextInput(attrs={'class' : 'form-control' , 'placeholder' : 'Aadhar No'}))
    phamail = forms.CharField(label = "" , widget = forms.TextInput(attrs={'class' : 'form-control' , 'placeholder' : 'Email'}))
    phaname = forms.CharField(label = "" , widget = forms.TextInput(attrs={'class' : 'form-control' , 'placeholder' : 'Name'}))
    phaaddr = forms.CharField(label = "" , widget = forms.TextInput(attrs={'class' : 'form-control' , 'placeholder' : 'Address'}))
    phaphone = forms.CharField(label = "" , widget = forms.TextInput(attrs={'class' : 'form-control' , 'placeholder' : 'Contact No'}))
