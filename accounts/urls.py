from django. urls import path, re_path
from . import views
from django.conf.urls import include

app_name='accounts'
urlpatterns = [
    path('login/', views.login_view.as_view(), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('registration/', views.registration_view.as_view(), name='registration'),
    path('likes/', views.liked_list.as_view(), name='liked_list'),
    path('messages/', views.messages_view.as_view(), name='messages'),
    path('messages/sent', views.messages_view.as_view(), name='messages_sent'),
    re_path(r'^messages/write/(?P<name>[\w.@+-]+|)/$', views.write_message_view.as_view(), name='write_message'),
    re_path(r'^messages/message/(?P<slug>[\w-]+)/$', views.message_view.as_view(), name='message'),
    re_path(r'^messages/message/(?P<slug>[\w-]+)/reply/$', views.reply_message_view.as_view(), name='reply_message'),
    path('messages/<str:order>/', views.messages_view.as_view(), name='messages'),
    path('messages/sent/<str:order>/', views.messages_view.as_view(), name='messages_sent'),
    path('profile/', views.profile_view.as_view(), name='profile'),
    path('db/seeding/plants', views.seed_plants, name='seed_plants'),
    path('db/cleaning/plants', views.clean_plants, name='clean_plants'),
    path('profile/delete', views.delete_profile, name='delete_profile'),
]
