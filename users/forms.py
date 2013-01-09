from django import forms
from django.contrib.auth.models import User
import re

class LoginForm(forms.Form):
    username = forms.CharField(max_length=20)
    password = forms.CharField(widget=forms.PasswordInput)

class RegisterForm(forms.Form):
    username = forms.CharField(max_length=20)
    password = forms.CharField(widget=forms.PasswordInput)
    rptpwd = forms.CharField(widget=forms.PasswordInput)
    idnum = forms.CharField(max_length=8)
    name = forms.CharField(max_length=20)
    teleph = forms.CharField(max_length=11)
    address = forms.CharField(max_length=50)

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('It has been used, please change another.')
        lenght = len(username)
        if lenght < 3:
            raise forms.ValidationError('It is too short, make it longer but less than 20.')
        else:
            m = re.match(r'^[\w_-]*$', username)
            if not m:
                raise forms.ValidationError('The valid input is digits,characters and "_ -"')
        return username

    def clean_rptpwd(self):
        pwd = self.cleaned_data['password']
        rptpwd = self.cleaned_data['rptpwd']
        if pwd != rptpwd:
            raise forms.ValidationError('Your passwords do not match!')
        return rptpwd

    def clean_idnum(self):
        idnum = self.cleaned_data['idnum']
        m = re.match(r'^\d{8}$', idnum)
        if not m:
            raise forms.ValidationError('It shold be 8 digits')
        return idnum

    def clean_teleph(self):
        teleph =self.cleaned_data['teleph']
        m = re.match(r'^\d{11}|\d{8}$', teleph)
        if not m:
            raise forms.ValidationError('It should be 11 or 8 digits')
        return teleph

class MdfinfoForm(forms.Form):
    idnum = forms.CharField(max_length=8, required=False)
    name = forms.CharField(max_length=20, required=False)
    teleph = forms.CharField(max_length=11,required=False)
    address = forms.CharField(max_length=50,required=False)

    def clean_teleph(self):
        teleph =self.cleaned_data['teleph']
        if teleph:
            m = re.match(r'^\d{11}|\d{8}$', teleph)
            if not m:
                raise forms.ValidationError('It should be 11 or 8 digits')
        return teleph

    def clean_idnum(self):
        idnum = self.cleaned_data['idnum']
        if idnum:
            m = re.match(r'^\d{8}$', idnum)
            if not m:
                raise forms.ValidationError('It shold be 8 digits')
        return idnum

class MdfpwdForm(forms.Form):
    oldpwd = forms.CharField(widget=forms.PasswordInput())
    newpwd = forms.CharField(widget=forms.PasswordInput())
    rptpwd = forms.CharField(widget=forms.PasswordInput())

    def clean_rptpwd(self):
        pwd = self.cleaned_data['newpwd']
        rptpwd = self.cleaned_data['rptpwd']
        if pwd != rptpwd:
            raise forms.ValidationError('Your passwords do not match!')
        return rptpwd