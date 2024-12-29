from django.contrib import admin
from django.urls import include, path

from . import battles

urlpatterns = [
    path('battles', views.login, name='login'),
    path('battles/<int:battle_id>', views.logout, name='logout'),
    path('battles/<int:battle_id>/<int:turn>', views.logout, name='logout'),
]
