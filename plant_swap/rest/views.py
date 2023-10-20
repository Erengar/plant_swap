from plant_collection.models import Species
from rest_framework import viewsets
from rest_framework import permissions
from rest.serializers import SpeciesSerializer

# Create your views here.

class SpeciesViewSet(viewsets.ModelViewSet):
    queryset = Species.objects.all().order_by('name')
    serializer_class = SpeciesSerializer
    permission_classes = [permissions.IsAuthenticated]