from plant_collection.models import Species, Plant
from rest_framework import viewsets
from rest_framework import permissions
from rest.serializers import SpeciesSerializer, PlantSerializer

# Create your views here.

class SpeciesViewSet(viewsets.ModelViewSet):
    queryset = Species.objects.all().order_by('name')
    serializer_class = SpeciesSerializer
    permission_classes = [permissions.IsAuthenticated]

class PlantViewSet(viewsets.ModelViewSet):
    queryset = Plant.objects.all().order_by('nick_name')
    serializer_class = PlantSerializer
    permission_classes = [permissions.IsAuthenticated]