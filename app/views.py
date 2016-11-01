from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import Profile,Education,Skills,Project
import smtplib
from django.contrib import messages
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
from django.utils.crypto import get_random_string
from .forms import EducationForm
# Create your views here.


def app_login(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            return redirect('app:dashboard')
        else:
            return render(request, 'login.html')

    elif request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            user = User.objects.get(username=username)
            if user.is_active:
                user = authenticate(username=username, password=password)
                if user is None:
                    return render(request, 'login.html', {'error': True, 'message': 'Please Provide Correct Username and Password'})
                else:
                    login(request, user)
                    return redirect('app:dashboard')
            else:
                return render(request, 'login.html', {'error': True, 'message': 'Please Verify Account First on email ' + user.email + ''})
        except:
            return render(request, 'login.html', {'error': True, 'message': 'Please Provide Correct Username and Password'})


def app_register(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            return redirect('app:dashboard')
        else:
            return render(request, 'register.html',{'error': False, 'message': ''})

    elif request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        first_name=request.POST.get('firstname')
        last_name=request.POST.get('lastname');
        if username=='' or password=='' or email=='' or first_name=='':
            return render(request, 'register.html', {'error': True, 'message': 'Please Fill All the Details'})
        try:
            user = User.objects.get(email=email)
            if user is not None:
                return render(request, 'register.html', {'error': True, 'message': 'Email Aready Taken'})
        except:
            try:
                user = User.objects.create_user(username, email, password)
                user.is_active = False
                user.first_name=first_name
                user.lastname=last_name
                user.save()
                activation_key = get_random_string(length=30)
                profile = Profile.objects.create(activation_key=activation_key,user=user);
                send_email(activation_key,email,1)
                return render(request, 'register.html', {'error': True, 'message': 'User Created Successfully.Verification Link sent to ' + user.email + ' .'})
            except Exception as e:
                print(e)
                return render(request, 'register.html', {'error': True, 'message': 'Username Already Taken'})
            else:
                return render(request, 'register.html', {'error': True, 'message': 'Email Aready Taken'})


def app_forgot_password(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            return redirect('app:dashboard')
        else:
            return render(request, 'forgot-password.html')
    elif request.method== 'POST':
        email=request.POST.get('fp_email')
        try:
            user=User.objects.get(email=email)
            try:
                newpass=get_random_string(length=8)
                user.set_password(newpass)
                user.save()
                send_email(newpass,user.email,2)
                return render(request,'forgot-password.html',{'error':True,'message':'Your Password Has been Succuessfully\
                    registred and has been sent to your registered Email'});
            except Exception as e:
                print(e)
        except:
            return render(request,'forgot-password.html',{'error':True,'message':'Email Not Registered With us'});

def app_change_password(request):
    if request.method=='GET':
        return render(request,'change-password.html')
    if request.method=='POST':
        current_password=request.POST.get("current_password")
        new_password=request.POST.get("new_password")
        confirm_password=request.POST.get("confirm_password")
        if current_password=='' or new_password=='' or confirm_password=='':
            return render(request,'change-password.html',{'error':True,'message':'Please Provide All The Details'})
        elif new_password!=confirm_password:
            return render(request,'change-password.html',{'error':True,'message':'Password Do Not Match'})
        elif len(new_password)<=6:
            return render(request,'change-password.html',{'error':True,'message':'Password Length Should be Greater than 6'})
        else:
            user=authenticate(username=request.user.username,password=current_password)
            if user is not None:
                print(new_password)
                user.set_password(new_password)
                user.save();
                return render(request,'change-password.html',{'error':True,'message':'Password Changed Successfully'})
            else:
                return render(request,'change-password.html',{'error':True,'message':'Please Provide Correct Password'})





def app_logout(request):
    logout(request)
    return redirect('app:login')


def app_dashboard(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            profile=Profile(user=request.user)
            educations=Education.objects.filter(profile=profile)
            skills=Skills.objects.filter(profile=profile)
            projects=Project.objects.filter(profile=profile)
            # educations=[{"name":"Xth","board":"CBSE","passing_year":"2010","percentage":80},{"name":"XIIth","board":"CBSE","passing_year":"2012","percentage":84},
            # {"name":"B.Tech","board":"IPU","passing_year":"2010","percentage":73}]
            # skills=['C','C++','Java','Mysql'];
            # projects=[{"description":"this is project1","url":"thisis url1"},{"description":"this is project1","url":"thisis url1"}]
            return render(request, 'profile.html',{'profile':profile,'user':request.user,'skills':skills,'projects':projects,"educations":educations})
        else:
            return redirect('app:login')

def app_verify(request,activation_key):
    if request.method=='GET':
        try:
            profile=Profile.objects.get(activation_key=activation_key)
            user=profile.user
            if user.is_active==False:
                user.is_active=True
                user.save();
                messages.add_message(request,messages.INFO,"You have been Successfully verified.Please Login To Continue")
                return redirect('app:login')
            else:
                messages.add_message(request,messages.INFO,'You have been already Verified.This Link Expires')
                return redirect('app:login')
        except Exception as e:
            messages.add_message(request,messages.INFO,"Please Register Youself First")
            return redirect('app:register')





def send_email(activation_key_or_newpass,email,task):


    to = email
    gmail_user = 'ritesh.bisht94@gmail.com'
    gmail_pwd = 'everythingis4me'
    smtpserver = smtplib.SMTP("smtp.gmail.com",587)
    smtpserver.ehlo()
    smtpserver.starttls()
    smtpserver.ehlo
    smtpserver.login(gmail_user, gmail_pwd)
    header = 'To:' + to + '\n' + 'From: ' + 'ritesh.bisht94@gmail.com'+ '\n' + 'Subject:testing \n'
    msg = MIMEMultipart('alternative')
    msg['Subject'] = "ProManage Verification Link"
    msg['From'] = "noreply@coronabpit.com"
    msg['To'] = to
    # Create the body of the message (a plain-text and an HTML version).
    if task==1:
        text = "Please Verify Your Accoutn on this link <a href='127.0.0./verify/"+activation_key+"'>Verify Your Account</a>"
       
    elif task==2:
        text="Your new Password is "+activation_key_or_newpass;
    part1 = MIMEText(text, 'html')
    msg.attach(part1)

    smtpserver.sendmail(gmail_user, to, msg.as_string())
    smtpserver.close()

def app_edit_profile(request):
    if request.method=='GET':
        form=EducationForm()
        return render(request, 'edit-profile.html', {'form': form})
