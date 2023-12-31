from django.contrib import admin
from .models import Plant, Species, Image


class ImageInline(admin.TabularInline):
    model = Image


class PlantAdmin(admin.ModelAdmin):
    inlines = [
        ImageInline,
    ]
    fieldsets = [
        (None, {
            'fields':['nick_name', 'species', 'owner', 'for_trade']
        })
    ]

admin.site.register(Plant, PlantAdmin)
admin.site.register(Species)
admin.site.register(Image)