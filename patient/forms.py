from django import forms
from .models import Patient
from django.shortcuts import render
from django.http import HttpResponseRedirect , HttpResponse
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.exceptions import NON_FIELD_ERRORS

class PatLogin(forms.Form) :
    username = forms.CharField(label = "" , widget = forms.TextInput(attrs={'class' : 'form-control' , 'placeholder' : 'Username'}))
    password = forms.CharField(label = 'Password' , max_length = 50 , widget = forms.PasswordInput(attrs={'class' : 'form-control' , 'placeholder' : 'Password'}))
    aadharno = forms.CharField(label = "" , widget = forms.TextInput(attrs={'class' : 'form-control' , 'placeholder' : 'Aadhar No'}))

class PatSignUp(forms.Form) :
    puser = forms.CharField(label = "" , widget = forms.TextInput(attrs={'class' : 'form-control' , 'placeholder' : 'Username'}))
    ppass1 = forms.CharField(label = 'Password' , max_length = 50 , widget = forms.PasswordInput(attrs={'class' : 'form-control' , 'placeholder' : 'Password'}))
    ppass2 = forms.CharField(label = 'Password' , max_length = 50 , widget = forms.PasswordInput(attrs={'class' : 'form-control' , 'placeholder' : 'Password'}))
    aadharno = forms.CharField(label = "" , widget = forms.TextInput(attrs={'class' : 'form-control' , 'placeholder' : 'Aadhar No'}))
    pmail = forms.CharField(label = "" , widget = forms.TextInput(attrs={'class' : 'form-control' , 'placeholder' : 'Email'}))
    pname = forms.CharField(label = "" , widget = forms.TextInput(attrs={'class' : 'form-control' , 'placeholder' : 'Name'}))
    pimage = forms.ImageField(required = True)
    page = forms.CharField(label = "" , widget = forms.TextInput(attrs={'class' : 'form-control' , 'placeholder' : 'Age'}))
    psx = forms.ChoiceField(choices = [('Male' , 'Male') , ('Female' , 'Female')] , widget = forms.Select(attrs={'class' : 'form-control'}))
    paddr = forms.CharField(label = "" , widget = forms.Textarea(attrs={'class' : 'form-control'}))
    pphone = forms.CharField(label = "" , widget = forms.TextInput(attrs={'class' : 'form-control' , 'placeholder' : 'Contact No'}))
    pnok = forms.CharField(label = "" , widget = forms.TextInput(attrs={'class' : 'form-control' , 'placeholder' : 'Next of Kin'}))
    pallerg = forms.CharField(label = "" , widget = forms.TextInput(attrs={'class' : 'form-control' , 'placeholder' : 'Allergies'}))
    pblood = forms.CharField(label = "" , widget = forms.TextInput(attrs={'class' : 'form-control' , 'placeholder' : 'Blood Group'}))
