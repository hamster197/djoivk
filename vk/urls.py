
from django.urls import path

from vk import views

app_name = 'vk'
urlpatterns = [
    path('', views.AuthInfoView, name='AuthInfo'),
    path('login/', views.LoginView, name='Login'),
]