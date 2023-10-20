from rest_framework import serializers
from plant_collection.models import Species

class SpeciesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Species
        fields = ('id', 'name')