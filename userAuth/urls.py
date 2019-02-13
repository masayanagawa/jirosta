from django.contrib import admin
from django.urls import include, path
from django.contrib.auth import views as auth_views

from . import views

app_name = "userAuth"
urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', views.login, name="login"),
    path('register/', views.register, name="register"),
    path('createuser/', views.create, name="create"),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]