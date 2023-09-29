from django import forms
from django.contrib.auth.models import User
from django.core.validators import MinLengthValidator
from .validators import unique_username, numbers_and_letters, upper_lower, unique_email
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.contrib.auth.forms import AuthenticationForm, UsernameField


class LoginForm(AuthenticationForm):
    username = UsernameField(label='User name',
                               widget=forms.TextInput(attrs={
                                   'class':'input'}))
    password = forms.CharField(label='Password',
                               strip=False,
                               widget=forms.TextInput(attrs={
                                    'class':'input',
                                    'type':'password',
                                    'autofocus':True,
                                    'autocomplete':'current-password'
    }))
                               
    class Meta:
        model = User


class RegistrationForm(forms.Form):
    error_css_class = 'is-danger'
    username = forms.CharField(label='User name',
                               validators=[unique_username,
                                           MinLengthValidator(4),
                                           UnicodeUsernameValidator],
                               max_length=14,
                               widget=forms.TextInput(attrs={
                                   'class':'input'
                            }))
    email = forms.EmailField(label='Email address',
                             validators=[unique_email],
                             widget=forms.TextInput(attrs={
                                 'class':'input',
                                 'type':'email'
                            }))
    password = forms.CharField(validators=[numbers_and_letters, upper_lower, MinLengthValidator(9)],
                                widget=forms.TextInput(attrs={
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
            raise forms.ValidationError('Password and Confirm password do not match!')