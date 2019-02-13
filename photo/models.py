from django.db import models
from django.utils import timezone

from user.models import FollowMaster

# Create your models here.

class PhotoMaster(models.Model):
    db_table = 'PhotoMaster'
    id = models.AutoField(verbose_name="id", max_length=100000, primary_key=True)
    photo = models.CharField(verbose_name="photo", max_length=100000, null=True)
    text = models.TextField(verbose_name="text", max_length=300, null=True)
    userid = models.CharField(verbose_name="userid", max_length=100000, null=True)
    date = models.DateTimeField(verbose_name="date", default=timezone.now)
