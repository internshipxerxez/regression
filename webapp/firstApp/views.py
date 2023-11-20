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
    smoker_input = request.GET['smoker'].lower()
    if smoker_input == 'yes':
        smoker_value=1
    elif smoker_input=='no':
        smoker_value=0
    else:
         return HttpResponse("Invalid input for 'smoker'. Please enter 'yes' or 'no'.")
     
    sex_input = request.GET['sex'].lower()
    if sex_input == 'male':
        sex_value=1
    elif sex_input=='no':
        sex_value=0
    else:
         return HttpResponse("Invalid input for 'sex'. Please enter 'male' or 'female'.")
     
    region_input = request.GET['region'].lower()
    if region_input== 'southwest':
        region_value=0
    elif region_input== 'southeast':
        region_value=1
    elif region_input== 'northwest':
        region_value=2
    elif region_input== 'northeast':
        region_value=3
    else:
         return HttpResponse("Invalid input for Region")

    list = []
    list.append(float(request.GET['age']))
    list.append(float(sex_value)),
    list.append(float(request.GET['bmi']))
    list.append(float(request.GET['children']))
    list.append(float(smoker_value)),
    list.append(float(region_value)),

    answer = model.predict([list]).tolist()[0]

    b = internship(age=request.GET['age'],sex=sex_value,bmi=request.GET['bmi'],children=request.GET['children'],smoker=smoker_value,
                   region=region_value,charges=answer)
    b.save()

    return render(request, "index.html", {'answer':answer})

################################## DEEP LEARNING ##########################

import keras
from PIL import Image
import numpy as np
import os
from django.core.files.storage import FileSystemStorage
import h5py as h5

media = 'media'
model = keras.models.load_model('trained.h5')


def makepredictions(path):
    img=Image.open(path)

    img_d = img.resize((255,255))

    if len(np.array(img_d).shape)<4:
        rgb_img=Image.new("RGB", img_d.size)
        rgb_img.paste(img_d)
    else:
        rgb_img=img_d

    rgb_img=np.array(rgb_img, dtype=np.float64)
    rgb_img=rgb_img.reshape(-1,255,255,3)

    predictions = model.predict(rgb_img)
    a = int(np.argmax(predictions))
    if a ==1 :
        a = "Result: glioma"
    elif a==2:
        a = "Result : meningioma"
    elif a == 3:
        a = "Result is : notumor"
    else:
        a = "Result : pituitary"
    return a



def index_deep(request):
    if request.method == "POST" and request.FILES['upload']:
        if 'upload' not in request.FILES:
            err = 'No Images Selected'
            return render(request, 'index_deep.html',{'err': err})
        f = request.FILES['upload']
        if f == '':
            err = 'No Files Selected'
            return render(request, 'index_deep.html', {'err': err})
        
        upload =request.FILES['upload']
        fss = FileSystemStorage()
        file = fss.save(upload.name,upload)
        file_url = fss.url(file)

        predictions = makepredictions(os.path.join(media, file))

        return render(request, 'index_deep.html', {'pred': predictions, 'file_url': file_url})
    else:
        return render(request, 'index_deep.html')


    
