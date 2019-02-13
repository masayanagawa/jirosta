from django.contrib import admin
from django.urls import include, path

from . import views

app_name = "app"
urlpatterns = [
    path('admin/', admin.site.urls),
    path('userAuth/', include('userAuth.urls')),
    path('top/', views.top, name="top"),
    path('upload/', views.upload, name="upload"),
    path('uploadpost/', views.uploadpost, name="uploadpost"),
    path('user/', include('user.urls')),
    path('setting/', include('setting.urls')),
]