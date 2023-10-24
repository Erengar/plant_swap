from django import forms
from .models import Plant, Species, Image
from .validators import unique_plant, image
from django.core.validators import MinLengthValidator


class add_plant_form(forms.ModelForm):
    nick_name = forms.CharField(
        max_length=24,
        validators=[unique_plant, MinLengthValidator(3)],
        widget=forms.TextInput(
            attrs={
                "class": "input",
            }
        ),
    )

    species = forms.ModelChoiceField(
        queryset=Species.objects,
        required=False,
        widget=forms.Select(
            attrs={
                "class": "select",
            }
        ),
    )
    for_trade = forms.BooleanField(required=False)

    class Meta:
        model = Plant
        fields = ("nick_name", "species", "for_trade")


class update_plant_form(add_plant_form):
    nick_name = forms.CharField(
        max_length=24,
        validators=[MinLengthValidator(3)],
        widget=forms.TextInput(
            attrs={
                "class": "input",
            }
        ),
    )


class image_form(forms.ModelForm):
    image = forms.ImageField(
        validators=[image],
        required=False,
        widget=forms.FileInput(
            attrs={
                "class": "input_tag0 file_input",
                "type": "file",
                "accept": "image/*",
                "hidden": "",
                "id": "input_tag0",
                "name": "picture0",
            }
        ),
    )

    class Meta:
        model = Image
        fields = ("image",)
