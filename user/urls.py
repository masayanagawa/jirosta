from django.contrib import admin
from django.urls import include, path

from . import views

app_name = "user"
urlpatterns = [
    path('', views.index, name="index"),
    path('search/', views.search, name="search"),
    path('searchuser/', views.searchuser, name="searchuser"),
    path('follow/', views.follow, name="follow"),
    path('unfollow/', views.unfollow, name="unfollow"),
    path('favorite/', views.favorite, name="favorite"),
    path('unfavorite/', views.unfavorite, name="unfavorite"),
]