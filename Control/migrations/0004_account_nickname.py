# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-05-22 10:46
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Control', '0003_auto_20170522_1845'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='nickname',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]