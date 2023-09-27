from django import forms
from django.contrib.auth.models import User
from django.core.validators import EmailValidator, validate_email

class LoginForm(forms.Form):
    username = forms.CharField(label='User name', max_length=20, help_text='username',
                               widget=forms.TextInput(attrs={
                                   'class':'input'}))
    password = forms.CharField(widget=forms.TextInput(attrs={
                                    'class':'input',
                                    'type':'password'
    }))
                               
    class Meta:
        model = User


class RegistrationForm(forms.Form):
    username = forms.CharField(label='User name',
                               max_length=20,
                               widget=forms.TextInput(attrs={
                                   'class':'input'
                            }))
    email = forms.EmailField(label='Email address',
                             validators=[validate_email],
                             widget=forms.TextInput(attrs={
                                 'class':'input',
                                 'type':'email'
                            }))
    password = forms.CharField(widget=forms.TextInput(attrs={
                                    'class':'input',
                                    'type':'password'
                            }))
    confirm_password = forms.CharField(widget=forms.TextInput(attrs={
                                            'class':'input',
                                            'type':'password'
                            }))

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def clean(self):
        data = super(RegistrationForm, self).clean()
        password = data.get('password')
        confirm_password = data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError('password and confirm_password does not match')
        