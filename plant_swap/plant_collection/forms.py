from django import forms
from .models import Plant, Species

class add_plant_form(forms.ModelForm):
    nick_name= forms.CharField(max_length=24,
                               widget=forms.TextInput(
                                   attrs={
                                       'class': 'input', 
                                   }))
    
    species= forms.ModelChoiceField(queryset=Species.objects,
                                    widget=forms.Select(
                                    attrs={
                                        'class':'select'
                                    }
    ))

    picture= forms.ImageField(widget=forms.FileInput(
                                    attrs={
                                        'class': 'file'
                                    }
    ))
    
    class Meta:
        model = Plant
        fields = ("nick_name", 'species', 'picture')

