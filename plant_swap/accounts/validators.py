from django import forms
from django.contrib.auth.models import User
import re

def unique_username(value):
    if User.objects.filter(username=value).exists():
        raise forms.ValidationError('Username already taken.')
    
def numbers_and_letters(value):
    if not (re.search('[a-z]+', value, flags=re.IGNORECASE) and re.search('[0-9]+', value)):
        raise forms.ValidationError('Password must contain letters and numbers.')
    
def upper_lower(value):
    if not(re.search('[a-z]+', value) and re.search('[A-Z]+', value)):
        raise forms.ValidationError('Password must contain at least one uppercase letter and one lowercase letter.')
    
def unique_email(value):
    if User.objects.filter(email=value).exists():
        raise forms.ValidationError('Email adress is already taken.')
    

def existing_user(value):
    if not User.objects.filter(username=value).exists():
        raise forms.ValidationError('User does not exist.')