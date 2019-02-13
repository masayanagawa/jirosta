from django.contrib import admin
from django.urls import include, path

from . import views

app_name = "setting"
urlpatterns = [
    path('', views.index, name="index"),
    path('post/', views.post, name="post"),
    path('password/', views.password, name="password"),
    path('postpassword/', views.postpassword, name="postpassword"),
    path('unregister', views.unregister, name="unregister")
]