from rest_framework import serializers
from plant_collection.models import Species, Plant

class SpeciesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Species
        fields = ('id', 'name')


class PlantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plant
        fields = ('id', 'nick_name', 'for_trade', 'created', 'owner', 'likes','picture')
        read_only_fields = ('created', 'owner', 'likes')


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plant
        fields = ('id', 'likes')
        read_only_fields = ('id',)