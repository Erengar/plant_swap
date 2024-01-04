from django.db import models
from django.core.validators import MinLengthValidator
from django.conf import settings
from django.utils.text import slugify
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import pre_save, post_delete
from pyuploadcare import Uploadcare


class Species(models.Model):
    name = models.CharField(max_length=64)
    slug = models.SlugField(default="bugged-species")

    def update_slug(self):
        self.slug = slugify(self.name)
        self.save()

    def save(self, *args, **kwargs):
        if self.slug != slugify(self.name):
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Plant(models.Model):
    nick_name = models.CharField(
        max_length=64, validators=[MinLengthValidator(3)], unique=True
    )
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated = models.DateTimeField(auto_now=True, null=True, blank=True)
    species = models.ForeignKey(
        Species, on_delete=models.SET_NULL, blank=True, null=True, related_name="plants"
    )
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="plants"
    )
    slug = models.SlugField(default="bugged-plant")
    for_trade = models.BooleanField(default=False)
    likes = models.ManyToManyField(User, related_name="liked")
    #This is far away from ideal, but it works for now
    location = models.CharField(max_length=24, blank=True, null=True, default=None, help_text="City, State")
    content = models.TextField(blank=True, null=True, default=None)

    def update_slug(self):
        self.slug = slugify(self.nick_name)
        self.save()

    def save(self, *args, **kwargs):
        if self.slug != slugify(self.nick_name):
            self.slug = slugify(self.nick_name)
        super().save(*args, **kwargs)

    def number_of_likes(self):
        return self.likes.count()

    def __str__(self):
        return self.nick_name


class Image(models.Model):
    plant = models.ForeignKey(Plant, on_delete=models.CASCADE, related_name="picture")
    image = models.CharField(max_length=256)

    def __str__(self):
        return str(self.pk)
    
@receiver(post_delete, sender=Image)
def delete_uploadcare_image(sender, instance, **kwargs):
    uploadcare = Uploadcare(public_key="f9c7bebe0949bee2838f", secret_key="3d390a60e900c30ee48b")
    file = uploadcare.file(instance.image)
    file.delete()

    
class Thumbnail(models.Model):
    plant = models.OneToOneField(Plant, on_delete=models.CASCADE, related_name="thumbnail")
    image = models.OneToOneField(Image, on_delete=models.CASCADE, related_name="thumbnail")

    def __str__(self):
        return str(self.pk)
