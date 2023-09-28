from django import forms
from django.contrib.auth.models import User
import re

def unique_username(value):
    if User.objects.filter(username=value):
        raise forms.ValidationError('Username taken.')
    
def numbers_and_letters(value):
    if not (re.search('[a-z]+', value, flags=re.IGNORECASE) and re.search('[0-9]+', value)):
        raise forms.ValidationError('Password must contain letters and numbers.')
    
def upper_lower(value):
    if not(re.search('[a-z]+', value) and re.search('[A-Z]+', value)):
        raise forms.ValidationError('Password must contain uppercase and lower case letters.')