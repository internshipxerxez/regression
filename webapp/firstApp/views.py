from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
import joblib
import json, os
import numpy as np
import pandas as pd
import psycopg2
from .models import internship

# Create your views here.

def index(request):
    return render(request, "index.html")

def SignupPage(request):
    if request.method=='POST':
        uname=request.POST.get('username')
        email=request.POST.get('email')
        pass1=request.POST.get('password1')
        pass2=request.POST.get('password2')

        if pass1!=pass2:
            return HttpResponse("Your password and conform password are not same !")
        else:
            my_user=User.objects.create_user(uname,email,pass1)
            my_user.save()
            return redirect('login')
    return render(request, 'signup.html')

def LoginPage(request):
    if request.method=='POST':
        username=request.POST.get('username')
        pass1=request.POST.get('pass1')

        user=authenticate(request, username=username, password=pass1)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            return HttpResponse ("Username or Password is incorrect !!!")
        
    return render (request, 'login.html')

def LogoutPage(request):
    logout(request)
    return redirect('login')


def result(request):
    model = joblib.load('../models/model.joblib')
    list = []
    list.append(float(request.GET['age']))
    list.append(float(request.GET['sex']))
    list.append(float(request.GET['bmi']))
    list.append(float(request.GET['children']))
    list.append(float(request.GET['smoker']))
    list.append(float(request.GET['region']))

    answer = model.predict([list]).tolist()[0]

    b = internship(age=request.GET['age'],sex=request.GET['sex'],bmi=request.GET['bmi'],children=request.GET['children'],smoker=request.GET['smoker'],
                   region=request.GET['region'],charges=answer)
    b.save()

    return render(request, "index.html", {'answer':answer})


    