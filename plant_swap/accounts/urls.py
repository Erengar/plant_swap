from django. urls import path
from . import views

app_name='accounts'
urlpatterns = [
    path('login/', views.login_view.as_view(), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('registration/', views.registration_view.as_view(), name='registration'),
    path('trades/', views.trades_view.as_view(), name='trades'),
    path('trades/<int:pk>/', views.trade_view.as_view(), name='trade'),
]
