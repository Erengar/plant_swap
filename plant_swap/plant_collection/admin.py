from django.contrib import admin
from .models import Plant, Species, Image

# Register your models here.

admin.site.register(Plant)
admin.site.register(Species)
admin.site.register(Image)