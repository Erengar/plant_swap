from django.urls import path
from . import views

app_name='plant_collection'
urlpatterns= [
    path('', views.front_page.as_view(), name='front_page'),
    path('like/', views.like_view, name='like'),
    path('page/<int:pagination>/', views.front_page.as_view(), name='front_page'),
    path('my-collection/', views.personal_collection.as_view(), name='personal_collection'),
    path('plant/<slug:slug>/', views.plant_view.as_view(),name='plant_view'),
    path('my-collection/add-plant/', views.add_plant.as_view(), name='add_plant'),
    path('plant/<slug:slug>/update/', views.update_plant.as_view(), name='update_plant'),
    path('species/', views.mobile_specie_search.as_view(), name='mobile_specie_search'),
    path('species/<slug:nam>/', views.species_list_view.as_view(), name='species_list'),
    path('species/search/bar/', views.search.as_view(), name='search'),
    path('trade/<str:req>', views.trade.as_view(), name='trade'),
    path('plant/<slug:slug>/plant-offers/', views.plant_offers.as_view(), name='plant_offers'),
]