# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-26 08:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin', '0002_logentry_remove_auto_add'),
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tempuser',
            name='user_ptr',
        ),
        migrations.AddField(
            model_name='profile',
            name='activation_key',
            field=models.CharField(default='', max_length=30),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='TempUser',
        ),
    ]
