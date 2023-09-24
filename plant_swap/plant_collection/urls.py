from django.urls import path
from . import views

app_name='plant_collection'
urlpatterns= [
    path('', views.front_page.as_view(), name='front_page'),
    path('plant_collection', views.personal_collection.as_view(), name='personal_collection'),
]