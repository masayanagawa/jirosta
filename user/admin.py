from django.contrib import admin

# Register your models here.

from .models import FollowMaster, FavoriteMaster

admin.site.register(FollowMaster)
admin.site.register(FavoriteMaster)