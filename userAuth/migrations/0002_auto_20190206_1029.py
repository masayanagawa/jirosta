# Generated by Django 2.1.2 on 2019-02-06 10:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userAuth', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='usermaster',
            name='profile',
            field=models.TextField(max_length=200, null=True, verbose_name='profile'),
        ),
        migrations.AddField(
            model_name='usermaster',
            name='username',
            field=models.CharField(max_length=30, null=True, verbose_name='username'),
        ),
    ]
