from django.db import models
from django.core.validators import MinLengthValidator
from django.conf import settings
from simple_history.models import HistoricalRecords
from django.utils.text import slugify
from django.contrib.auth.models import User
# Create your models here.

class Species(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name



class Plant(models.Model):
    nick_name = models.CharField(
        max_length=64,
        validators=[MinLengthValidator(3)],
        unique=True)
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated = models.DateTimeField(auto_now=True, null=True, blank=True)
    species = models.ForeignKey(Species, on_delete=models.PROTECT, blank=True, null=True, related_name='plants')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='plants')
    slug = models.SlugField(default='bugged-plant')
    for_trade = models.BooleanField(default=False)
    likes = models.ManyToManyField(User, related_name= 'liked')
    #history = HistoricalRecords(excluded_fields=['tags', 'species', 'nick_name', 'updated'])

    def update_slug(self):
        self.slug = slugify(self.nick_name)
        self.save()

    def save(self, *args, **kwargs):
        if self.slug != slugify(self.nick_name):
            self.slug=slugify(self.nick_name)
        super().save(*args, **kwargs)

    def number_of_likes(self):
        return self.likes.count()

    def __str__(self):
        return self.nick_name
    

class Image(models.Model):
    plant = models.ForeignKey(Plant, on_delete=models.CASCADE, related_name='picture')
    image = models.ImageField(upload_to='pics')

    def __str__(self):
        return str(self.plant.nick_name) + ' ' + str(self.pk)