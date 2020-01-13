from django.shortcuts import render
from django.urls import path, include
from . import views
from django.conf import settings
# Create your views here.
urlpatterns = [
    path('', views.register, name='register'),
    path('login', views.login, name='login'),
    path('registration', views.registration, name='registration'),
    path('login_', views.login_, name='login_'),
    path('success',views.success,name='success')
]

