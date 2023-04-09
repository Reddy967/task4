import random

from django.shortcuts import render, redirect
from .models import *
from .mixins import MessaHandler
from django.contrib.auth import login

# Create your views here.
def login_view(request):
    if request.method == 'POST':
        phone_number = request.POST.get('phone_number')
        profile = Profile.objects.filter(phone_number=phone_number)
        if not profile.exists():
            return redirect('/register/')

        profile[0].otp = random.randint(1000, 9999)
        profile[0].save()
        message_handler = MessaHandler().send_otp_on_phone()
        return redirect(f'/otp/{profile[0].uid}')
    return render(request,'login.html')

def register_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        gender = request.POST.get('gender')
        phone_number = request.POST.get('phone_number')
        user = User.objects.create(email=email, first_name=first_name, last_name=last_name)
        profile = Profile.objects.create(user=user, phone_number=phone_number, gender=gender)

        return redirect('/')
    return render(request,'register.html')

def dashboard_view(request):
    return render(request,'dashboard.html')

def otp(request, uid):
    if request.method == 'POST':
        otp = request.POST.get('otp')
        profile = Profile.objects.get(uid=uid)
        if otp == profile.otp:
            login(request, profile.user)
            return redirect('/dashboard/')
        return redirect(f'/otp/{uid}')
    return render(request,'otp.html')
