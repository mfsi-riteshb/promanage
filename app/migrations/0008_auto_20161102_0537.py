# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-02 05:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_auto_20161028_0550'),
    ]

    operations = [
        migrations.AddField(
            model_name='education',
            name='board_university',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AddField(
            model_name='profile',
            name='gender',
            field=models.CharField(choices=[('Male', 'Male'), ('Female', 'Female')], default='M', max_length=10),
        ),
    ]
