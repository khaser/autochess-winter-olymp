from django.contrib import admin
from django.urls import include, path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:battle_id>/<int:turn>', views.details, name='details'),
    path('<int:battle_id>/-<int:turn>', views.details_neg, name='details_neg'),
    path('planning', views.planning, name='planning'),
    path('rules', views.lore, name='lore'),
    path('rules/lore', views.lore, name='lore'),
    path('rules/combat', views.combat, name='combat'),
    path('rules/monsters', views.monsters, name='monsters'),
    path('scores', views.scores, name='scores'),
]
