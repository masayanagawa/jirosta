from django.db import models

# Create your models here.

class UserMaster(models.Model):
    db_table = 'UserMaster'
    id = models.AutoField(verbose_name="id", max_length=100000, primary_key=True)
    userid = models.CharField(verbose_name="userid", max_length=50, unique=True, null=True)
    password = models.CharField(verbose_name="password", max_length=32)
    username = models.CharField(verbose_name="username", max_length=30, null=True)
    profile = models.TextField(verbose_name="profile", max_length=200, null=True)
