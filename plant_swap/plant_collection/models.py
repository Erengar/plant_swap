from django.db import models
from django.core.validators import MinLengthValidator
from django.conf import settings
from django.utils.text import slugify
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import pre_save, post_delete


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
    image = models.ImageField(upload_to="pics")

    def __str__(self):
        return str(self.pk)


class Trade(models.Model):
    plant_offered = models.ForeignKey(
        Plant, on_delete=models.CASCADE, related_name="trades_offered"
    )
    plant_requested = models.ForeignKey(
        Plant, on_delete=models.CASCADE, related_name="trades_requested"
    )
    initiator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="trades_initiated",
    )
    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="trades_received",
    )
    accepted = models.BooleanField(null=True, blank=True)
    offered_finalized = models.BooleanField(default=False)
    requested_finalized = models.BooleanField(default=False)
    finalized = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    class Meta:
        unique_together = ["plant_offered", "plant_requested"]

    def accept(self):
        self.accepted = True
        self.save()

    def decline(self):
        self.accepted = False
        self.delete()

    def exchange(self):
        self.plant_offered.owner = self.recipient
        self.plant_requested.owner = self.initiator
        self.plant_offered.save()
        self.plant_requested.save()

    def __str__(self):
        return f"{self.plant_offered} for {self.plant_requested}"
    
class Thumbnail(models.Model):
    plant = models.OneToOneField(Plant, on_delete=models.CASCADE, related_name="thumbnail")
    image = models.OneToOneField(Image, on_delete=models.CASCADE, related_name="thumbnail")

    def __str__(self):
        return str(self.pk)


@receiver(post_delete, sender=Image)
def post_save_image(sender, instance, *args, **kwargs):
    """Clean Old Image file"""
    try:
        instance.image.delete(save=False)
    except:
        pass


@receiver(pre_save, sender=Image)
def pre_save_image(sender, instance, *args, **kwargs):
    """instance old image file will delete from os"""
    try:
        old_img = instance.__class__.objects.get(id=instance.id).image.path
        try:
            new_img = instance.image.path
        except:
            new_img = None
        if new_img != old_img:
            import os

            if os.path.exists(old_img):
                os.remove(old_img)
    except:
        pass
