# Generated by Django 2.2.13 on 2020-07-24 07:18

import bboard.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bboard', '0009_auto_20200724_0610'),
    ]

    operations = [
        migrations.AlterField(
            model_name='img',
            name='img',
            field=models.ImageField(upload_to=bboard.models.get_timestamp_path, verbose_name='Изображение'),
        ),
    ]
