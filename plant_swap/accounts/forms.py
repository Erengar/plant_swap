from django import forms
from django.contrib.auth.models import User

class LoginForm(forms.Form):
    username = forms.CharField(label='User name', max_length=20)
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = User


class RegistrationForm(forms.Form):
    username = forms.CharField(label='User name', max_length=20)
    email = forms.EmailField(label='Email address')
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def clean(self):
        data = super(RegistrationForm, self).clean()
        password = data.get('password')
        confirm_password = data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError('password and confirm_password does not match')
        