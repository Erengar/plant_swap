from django.db import models
from django.core.validators import MinLengthValidator
from django.conf import settings
from simple_history.models import HistoricalRecords
# Create your models here.

class Species(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name



class Plant(models.Model):
    nick_name = models.CharField(
        max_length=64,
        validators=[MinLengthValidator(3)])
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated = models.DateTimeField(auto_now=True, null=True, blank=True)
    species = models.ForeignKey(Species, on_delete=models.PROTECT, related_name='plants')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    picture = models.ImageField(upload_to='static/images/', null=True, blank=True)
    #history = HistoricalRecords(excluded_fields=['tags', 'species', 'nick_name', 'updated'])

    def __str__(self):
        return self.nick_name