# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-03 10:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0009_auto_20161103_1008'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='home_address',
            field=models.CharField(default=None, max_length=50),
        ),
    ]
