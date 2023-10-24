from django.urls import path, include
from rest_framework import routers
from rest import views

router = routers.DefaultRouter()
router.register(r'species', views.SpeciesViewSet)
router.register(r'plants', views.PlantViewSet)
router.register(r'likes', views.LikeViewSet, basename='likes')

urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
