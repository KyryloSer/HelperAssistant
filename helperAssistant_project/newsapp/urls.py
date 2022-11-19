from django.urls import path
from . import views

urlpatterns = [
    path('', views.news_main, name='news_main'),
    path('war/', views.news_war, name='news_war'),
    path('society/', views.news_society, name='news_society'),
    path('world/', views.news_world, name='news_world'),
    path('politics/', views.news_politics, name='news_politics'),
    path('science/', views.news_science, name='news_science'),
    path('techno/', views.news_techno, name='news_techno'),
    path('weather/', views.news_weather, name='news_weather'),
    path('fuel/', views.news_fuel, name='news_fuel'),
    path('currency/', views.news_currency, name='news_currency'),
    ]
