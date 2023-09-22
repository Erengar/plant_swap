from django.urls import path
from . import views

app_name='plant_collection'
urlpatterns= [
    path('', views.personal_collection.as_view(), name='personal_collection'),
]