from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import Profile, Education, Skills, Project
from django.core.mail import send_mail
from django.contrib import messages
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
from django.utils.crypto import get_random_string
from .forms import ( 
    EducationForm, RegisterForm, ChangePasswordForm,
    MyPasswordResetForm, MySetPasswordForm, MyPasswordChangeForm
    )
from django.contrib.auth import views
from django.views import View
from django.contrib.auth.tokens import ( PasswordResetTokenGenerator,
                                         default_token_generator
                                        )
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin

from django.core.urlresolvers import reverse
from django.contrib.auth.views import (
    password_reset, password_reset_done, password_reset_confirm, 
    password_reset_complete
    )
from django.contrib.auth import views as auth_views

# Create your views here.


class LoginView(View):

    """
    This Class handles the GET/POST Request of Login Task
    """

    template_name = "login.html"
    redirect_url = "app:dashboard"

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(self.redirect_url)
        else:
            return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                return views.login(request, template_name=self.template_name)
            else:
                return render(request, 'login.html', 
                              {'error': True, 'message': 'Please Verify Account\
                               First on email ' + user.email + ''})
        else:
            return render(request, 'login.html', {'error': True, 
                          'message': 'Please\Provide Correct Username and Password'})


class RegisterView(View):

    """
    This class handles POST/GET request for User Registration Task
    """

    template_name = "register.html"
    form = RegisterForm()

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('app:dashboard')
        else:
            print(self.form)
            return render(request, self.template_name, {'form': self.form})

    def post(self, request, *args, **kwargs):
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        register_form = RegisterForm(request.POST)
        print(register_form.is_valid())
        if not register_form.is_valid():
            print(register_form.errors)
            return render(request, self.template_name, {'form': register_form})
        user = User.objects.create_user(username, email, password)
        user.is_active = False
        user.first_name = first_name
        user.last_name = last_name
        user.save()
        activation_key = get_random_string(length=30)
        profile = Profile.objects.create(
            activation_key=activation_key, user=user)
        text = "Please Verify Your Accoutn on this link <a href='127.0.0.1/verify/" + \
        activation_key + "'>Verify Your Account</a>"
        user.email_user("Please verify Your account",text,"Promanage");
        messages.add_message(request, messages.INFO, 
                            'User Created Successfully.Verification \
                            Link sent to ' + user.email + ' .')
        return render(request, self.template_name, {'form': self.form})


class PasswordChangeView(View):

    """
    This Class handle GET/POST Request for changing password
    """

    template_name = 'password_change_form.html'

    def get(self, request, *args, **kwargs):
        return auth_views.password_change(request,template_name=self.template_name,
                                          post_change_redirect="app:password_change_done",
                                          password_change_form=MyPasswordChangeForm,
                                          current_app=None,
                                          extra_context=None)

    def post(self, request, *args, **kwargs):
        return auth_views.password_change(request, template_name=self.template_name,
                                          post_change_redirect="app:password_change_done",
                                          password_change_form=MyPasswordChangeForm, current_app=None,
                                          extra_context=None)


class PasswordChangeDoneView(View):

    """
    This Class handles the GET Request To display success of Password change
    """

    template_name = 'password_change_done.html'

    def get(self, request, *args, **kwargs):
        return auth_views.password_change_done(request,
                                               template_name=self.template_name,
                                               current_app=None, extra_context=None)


class PasswordResetView(UserPassesTestMixin,View):

    """
    This Class handles the GET?POST Request To handle Password Reset and sending mail to emailid.
    """
    login_url="app:login"
    template_name = 'password_reset.html'
    form = MyPasswordResetForm

    def test_func(self):
        return  not self.request.user.is_authenticated

    def get(self, request, *args, **kwargs):
         return auth_views.password_reset(request, template_name=self.template_name,
                                         email_template_name="password_reset_email.html",   
                                         password_reset_form=MyPasswordResetForm,
                                         post_reset_redirect="app:password_reset_done")

    def post(self, request, *args, **kwargs):
        return auth_views.password_reset(request, template_name=self.template_name,
                                        email_template_name="password_reset_email.html",   
                                        password_reset_form=MyPasswordResetForm,
                                        post_reset_redirect="app:password_reset_done")


class PasswordResetDoneView(View):

    """
    This Class handles the GET Request To display PAssword Link Successfully sent page.
    """
    template_name='password_reset_done.html'
    def get(self, request, *args, **kwargs):
        return auth_views.password_reset_done(request, template_name=self.template_name,
                                              current_app=None, extra_context=None)


class PasswordResetConfirmView(View):

    """
    This Class handles get/post request,display form and handle setting new password.
    """

    template_name = 'password_reset_confirm.html'

    def get(self, request, *args, **kwargs):
        return auth_views.password_reset_confirm(request, uidb64=self.kwargs['uidb64'],
                                                token=self.kwargs['token'], 
                                                template_name=self.template_name,
                                                token_generator=default_token_generator,
                                                set_password_form=MySetPasswordForm,
                                                post_reset_redirect="app:password_reset_complete", 
                                                current_app=None, extra_context=None)

    def post(self, request, *args, **kwargs):
        return auth_views.password_reset_confirm(request, uidb64=self.kwargs['uidb64'],
                                                token=self.kwargs['token'], 
                                                template_name=self.template_name,
                                                token_generator=default_token_generator, 
                                                set_password_form=MySetPasswordForm,
                                                post_reset_redirect="app:password_reset_complete", 
                                                current_app=None, extra_context=None)


class PasswordResetCompleteView(View):

    """
    This Class handles GET Request and display password changed successfully
    """

    template_name = 'password_reset_complete.html'

    def get(self, request, *args, **kwargs):
        print("hello")
        return password_reset_complete(request,
                                       template_name=self.template_name,
                                       current_app=None, extra_context=None)



class LogoutView(View):
    """
    This class Handle  Request for logout 
    """
    def get(self, request, *args, **kwargs):
        views.logout(request, next_page="app:login")
        return redirect('app:login')


class DashBoardView(LoginRequiredMixin, View):

    """
    This Class Handles the GET Request  for displaying profile page
    """

    login_url = '/login'
    redirect_field_name = None
    template_name = "profile.html"

    def get(self, request, *args, **kwargs):
        profile = Profile.objects.get(user=request.user)
        educations = Education.objects.filter(profile=profile)
        print(list(educations))
        skills = Skills.objects.filter(profile=profile)
        projects = Project.objects.filter(profile=profile)
        return render(request, self.template_name, {'profile': profile, 
                      'user': request.user, 'skills': skills, 'projects':
                       projects, "educations": educations})



class AccountVerifyView(View):

    """
    This Class Handle GET Request for verification of account.
    """

    def get(self, request, *args, **kwargs):
        try:
            profile = Profile.objects.get(activation_key=self.kwargs['activation_key'])
            user = profile.user
            if user.is_active == False:
                user.is_active = True
                user.save()
                messages.add_message(
                    request, messages.INFO, "You have been Successfully verified\
                    .Please Login To Continue")
                return redirect('app:login')
            else:
                messages.add_message(
                    request, messages.INFO, 'You have been already Verified.This\
                     Link Expires')
                return redirect('app:login')
        except Exception as e:
            messages.add_message(request, messages.INFO,
                                 "Please Register Youself First")
            return redirect('app:register')
       


class EditProfileView(View):
    
    def get(self, request, *args, **kwargs):
        form = EducationForm()
        return render(request, 'edit-profile.html', {'form': form})

    def post(self, request, *args, **kwargs):
        pass



