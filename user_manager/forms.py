from django import forms
from django.contrib.auth import models 
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm,UsernameField,PasswordChangeForm,PasswordResetForm,SetPasswordForm
from django.contrib.auth.models import User
from django.forms import fields
from django.forms import widgets
from django.forms.models import ModelForm
from django.utils.translation import gettext,gettext_lazy as _
from django.contrib.auth import authenticate,login,logout
from django.forms.widgets import EmailInput, PasswordInput, TextInput



class MySetPasswordForm(SetPasswordForm):
     new_password1=forms.CharField(label=_('New Password'),strip=False,widget=forms.PasswordInput(attrs={'autocomplete':'new-password','class':'form-control'}))
     new_password2= forms.CharField(label=_('confirm New Password'),strip=False,widget=forms.PasswordInput(attrs={'autocomplete':'new-password','class':'form-control'}))  

class PasswordChange(PasswordChangeForm):
    old_password=forms.CharField(label='Old Password',widget=forms.PasswordInput(attrs={'class':'form-control'}))
    new_password1=forms.CharField(label='New Password',widget=forms.PasswordInput(attrs={'class':'form-control'}))
    new_password2=forms.CharField(label='New Password',widget=forms.PasswordInput(attrs={'class':'form-control'}))
    
class RestForm(PasswordResetForm):
    email=forms.EmailField(label=_("Email"), required=True,max_length=254,widget=EmailInput(attrs={'class':'form-control'}))