from django.urls import path
from . import views

app_name='plant_collection'
urlpatterns= [
    path('', views.front_page.as_view(), name='front_page'),
    path('like/', views.like_view, name='like'),
    path('my-collection/', views.personal_collection.as_view(), name='personal_collection'),
    path('my-collection/page/<int:pagination>/', views.personal_collection.as_view(), name='personal_collection'),
    path('my-collection/<str:order>/page/<int:pagination>/', views.personal_collection.as_view(), name='personal_collection'),
    path('plant/<slug:slug>/', views.plant_view.as_view(),name='plant_view'),
    path('my-collection/add-plant/', views.add_plant.as_view(), name='add_plant'),
    path('plant/<slug:slug>/update/', views.update_plant.as_view(), name='update_plant'),
    path('species/', views.mobile_specie_search.as_view(), name='mobile_specie_search'),
    path('species/search/bar/', views.search.as_view(), name='search'),
    path('species/search/bar/<str:specie>', views.search.as_view(), name='search'),
    path('<str:order>/page/<int:pagination>/', views.front_page.as_view(), name='front_page'),
    path('<slug:specie>/<str:order>/page/<int:pagination>/', views.front_page.as_view(), name='front_page'),
    path('search=<str:search>/<str:order>/page/<int:pagination>/', views.front_page.as_view(), name='front_page'),
        path('my-collection/search=<str:search>/<str:order>/page/<int:pagination>/', views.personal_collection.as_view(), name='personal_collection'),
    path('<slug:specie>/search=<str:search>/<str:order>/page/<int:pagination>/', views.front_page.as_view(), name='front_page'),
]