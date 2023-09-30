from django import forms
from .models import Plant, Species
from .validators import unique_plant, image
from django.core.validators import MinLengthValidator

class add_plant_form(forms.ModelForm):
    nick_name= forms.CharField(max_length=24,
                               validators=[unique_plant, MinLengthValidator(3)],
                               widget=forms.TextInput(
                                   attrs={
                                       'class': 'input', 
                                   }))
    

    species= forms.ModelChoiceField(queryset=Species.objects,
                                    required=False,
                                    widget=forms.Select(
                                    attrs={
                                        'class':'select'
                                    }
    ))
    for_trade = forms.BooleanField()

    class Meta:
        model = Plant
        fields = ("nick_name", 'species')

'''
    picture= forms.ImageField(validators=[image],
                              widget=forms.FileInput(
                                    attrs={
                                        'class': 'file-input',
                                        'type':'file',
                                        'accept':'image/jpeg, image/png, image/jpg'
                                    }
    ))'''