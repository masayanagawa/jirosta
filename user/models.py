from django.db import models
from django.utils import timezone
# Create your models here.

class FollowMaster(models.Model):
    db_table = 'FollowMaster'
    id = models.AutoField(verbose_name="id", max_length=100000, primary_key=True)
    followid = models.CharField(verbose_name="followid", max_length=50, null=True)
    userid = models.CharField(verbose_name="userid", max_length=50, null=True)
    date = models.DateTimeField(verbose_name="date", default=timezone.now)

class FavoriteMaster(models.Model):
    db_table = 'FavoriteMaster'
    id = models.AutoField(verbose_name="id", max_length=100000, primary_key=True)
    favoriteid = models.CharField(verbose_name="favoriteid", max_length=50, null=True)
    userid = models.CharField(verbose_name="userid", max_length=50, null=True)
    date = models.DateTimeField(verbose_name="date", default=timezone.now)