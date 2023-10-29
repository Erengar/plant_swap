from django import forms
from .models import Plant


def unique_plant(value):
    if Plant.objects.filter(nick_name=value).exists():
        raise forms.ValidationError("Nickname already taken.")


def image(value):
    if not value:
        raise forms.ValidationError("You must provide at least 1 image.")
