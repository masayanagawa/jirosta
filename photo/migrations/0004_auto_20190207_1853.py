# Generated by Django 2.1.2 on 2019-02-07 09:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('photo', '0003_photomaster_text'),
    ]

    operations = [
        migrations.AlterField(
            model_name='photomaster',
            name='photo',
            field=models.ImageField(max_length=100000, null=True, upload_to='', verbose_name='photo'),
        ),
    ]
