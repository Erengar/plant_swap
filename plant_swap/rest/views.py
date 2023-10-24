from plant_collection.models import Species, Plant
from rest_framework import viewsets
from rest_framework import permissions
from rest.serializers import SpeciesSerializer, PlantSerializer, LikeSerializer
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from django.views.decorators.cache import cache_page


class SpeciesViewSet(viewsets.ModelViewSet):
    queryset = Species.objects.all().order_by('name')
    serializer_class = SpeciesSerializer
    permission_classes = [permissions.IsAuthenticated]

class PlantViewSet(viewsets.ModelViewSet):
    queryset = Plant.objects.all().order_by('nick_name')
    serializer_class = PlantSerializer
    permission_classes = [permissions.IsAuthenticated]

class LikeViewSet(viewsets.ViewSet):
    def list(self, request, pk=None):
        queryset = Plant.objects.filter(pk=pk)
        serializer = LikeSerializer(queryset, many=True)
        return Response(serializer.data)
    
    def update(self, request, pk=None):
        plant = get_object_or_404(Plant, pk=pk)
        user = request.user
        if user in plant.likes.all():
            plant.likes.remove(user)
        else:
            plant.likes.add(user)
        plant.save()
        serializer = LikeSerializer(plant)
        return Response(serializer.data)