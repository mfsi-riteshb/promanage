from django.forms import ModelForm
from .models import Education, Profile, User
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import (
    AuthenticationForm, PasswordChangeForm, PasswordResetForm, SetPasswordForm,
)


class EducationForm(ModelForm):

    class Meta:
        model = Education
        fields = ['name', 'board_university', 'passing_year', 'percentage']


class MyPasswordChangeForm(PasswordChangeForm):

    old_password = forms.CharField(label=("Old password"),
                                   widget=forms.PasswordInput(
        attrs={'class': 'form-control',
               'id': 'old_password1'}))
    new_password1 = forms.CharField(label=("New password"),
                                    widget=forms.PasswordInput(
                                        attrs={'class': 'form-control',
                                               'id': 'new_password1'}))
    new_password2 = forms.CharField(label=("New password confirmation"),
                                    widget=forms.PasswordInput(
        attrs={'class': 'form-control',
               'id': 'new_password2'}
    )
    )


class MyPasswordResetForm(PasswordResetForm):

    email = forms.EmailField(max_length=30, required=True, widget=forms.EmailInput(
        attrs={'class': 'form-control', 'placeholder': 'email', 'id': 'email'}))

    def clean_email(self):
        email = self.cleaned_data['email']
        if not User.objects.filter(email__iexact=email, is_active=True).exists():
            raise forms.ValidationError(
                "There is no user registered with the specified email address!")

        return email


class MySetPasswordForm(SetPasswordForm):

    new_password1 = forms.CharField(label=("New password"),
                                    widget=forms.PasswordInput(
        attrs={'class': 'form-control',
               'id': 'new_password1'}))
    new_password2 = forms.CharField(label=("New password confirmation"),
                                    widget=forms.PasswordInput(
                                        attrs={'class': 'form-control',
                                               'id': 'new_password2'}
    )
    )


class ChangePasswordForm(forms.Form):

    current_password = forms.CharField(max_length=30,
                                       required=True,
                                       widget=forms.PasswordInput(
                                           attrs={'class': 'form-control',
                                                  'placeholder': 'current_password',
                                                  'id': 'current_password'}
                                       )
                                       )
    new_password = forms.CharField(max_length=30,
                                   required=True,
                                   widget=forms.PasswordInput(
                                       attrs={'class': 'form-control',
                                              'placeholder': 'new password',
                                              'id': 'new_password'}))
    cpassword = forms.CharField(max_length=30,
                                required=True,
                                widget=forms.PasswordInput(
                                    attrs={'class': 'form-control', 'placeholder':
                                           'confirm password', 'id': 'cpassword'}
                                )
                                )

    def clean_cpassword(self):
        password1 = self.cleaned_data.get('new_password')
        password2 = self.cleaned_data.get('cpassword')
        print(password1)
        print(password2)
        if not password2:
            raise forms.ValidationError("You must confirm your password")
        if password1 != password2:
            raise forms.ValidationError("Your passwords do not match")
        return password2


class RegisterForm(ModelForm):

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password',)
        fields_required = ('username', 'email', 'first_name', 'last_name')
        widgets = {
            'username': forms.TextInput(attrs={'required': 'false',
                                               'class': 'form-control',
                                               'placeholder': 'username',
                                               'id': 'username'}),
            'first_name': forms.TextInput(attrs={'required': 'false',
                                                 'class': 'form-control',
                                                 'placeholder': 'firstname',
                                                 'id': 'firstname'}),
            'last_name': forms.TextInput(attrs={'required': 'false',
                                                'class': 'form-control',
                                                'placeholder': 'lastname',
                                                'id': 'lastname'}),
            'email': forms.EmailInput(attrs={'required': 'false',
                                             'class': 'form-control',
                                             'placeholder': 'email',
                                             'id': 'email'}),
            'password': forms.PasswordInput(attrs={'required': 'false',
                                                   'class': 'form-control',
                                                   'placeholder': 'password',
                                                   'id': 'password'}),
            'cpassword': forms.PasswordInput(attrs={'required': 'false',
                                                    'class': 'form-control',
                                                    'placeholder': 'confirm password',
                                                    'id': 'cpassword'})
        }

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, *kwargs)
        self.fields['cpassword'] = forms.CharField(widget=forms.PasswordInput(
                                                   attrs={'class': 'form-control',
                                                          'placeholder': 'confirm password',
                                                          'id': 'cpassword'}))
        for key in self.fields:
            self.fields[key].required = True

    def clean_email(self):
        email = self.cleaned_data['email']
        try:
            user = User.objects.get(email=email)
            raise forms.ValidationError("This Email is Already Taken")
        except User.DoesNotExist:
            return email
