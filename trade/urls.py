from django.urls import path
from . import views

app_name='trades'

urlpatterns = [
    path('<str:req>', views.trade.as_view(), name='trade'),
    path('<slug:slug>/plant-offers/', views.plant_offers.as_view(), name='plant_offers'),
    path('', views.trades_view.as_view(), name='trades'),
    path('<int:pk>/', views.trade_final.as_view(), name='trade_final'),
]
