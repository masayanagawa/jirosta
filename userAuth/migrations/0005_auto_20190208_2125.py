# Generated by Django 2.1.2 on 2019-02-08 12:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userAuth', '0004_remove_usermaster_imgname'),
    ]

    operations = [
        migrations.AddField(
            model_name='usermaster',
            name='userid',
            field=models.CharField(max_length=50, null=True, verbose_name='userid'),
        ),
        migrations.AlterField(
            model_name='usermaster',
            name='id',
            field=models.AutoField(max_length=100000, primary_key=True, serialize=False, verbose_name='id'),
        ),
    ]
