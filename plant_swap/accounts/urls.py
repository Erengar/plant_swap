from django. urls import path
from . import views

app_name='accounts'
urlpatterns = [
    path('login/', views.login_view.as_view(), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('registration/', views.registration_view.as_view(), name='registration')
]
