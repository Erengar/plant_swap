from django.urls import path
from . import views

app_name='plant_collection'
urlpatterns= [
    path('', views.front_page.as_view(), name='front_page'),
    path('my-collection/', views.personal_collection.as_view(), name='personal_collection'),
    path('<slug:slug>/', views.plant_view.as_view(),name='plant_view'),
    path('my-collection/add-plant', views.add_plant.as_view(), name='add_plant'),
]