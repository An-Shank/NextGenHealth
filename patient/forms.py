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
