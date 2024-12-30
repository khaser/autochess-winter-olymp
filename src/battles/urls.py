from django.contrib import admin
from django.urls import include, path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:battle_id>/<int:turn>', views.details, name='details'),
    # TODO: 303 into /battles/<id>/0
    # path('battles/<int:battle_id>', views.logout, name='logout'),
]
