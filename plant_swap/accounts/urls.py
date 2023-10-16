from django. urls import path, re_path
from . import views
from django.conf.urls import include

app_name='accounts'
urlpatterns = [
    path('login/', views.login_view.as_view(), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('registration/', views.registration_view.as_view(), name='registration'),
    path('trades/', views.trades_view.as_view(), name='trades'),
    path('trades/<int:pk>/', views.trade_view.as_view(), name='trade'),
    path('likes/', views.liked_list.as_view(), name='liked_list'),
    path('', include('social_django.urls', namespace='social')),
    path('messages/', views.messages_view.as_view(), name='messages'),
    re_path(r'^messages/write/(?P<name>[\w.@+-]+|)/$', views.write_message_view.as_view(), name='write_message'),
    re_path(r'^messages/message/(?P<slug>[\w-]+)/$', views.message_view.as_view(), name='message'),
    re_path(r'^messages/message/(?P<slug>[\w-]+)/reply/$', views.reply_message_view.as_view(), name='reply_message'),
]
