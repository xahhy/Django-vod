# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-04-17 09:40
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vodmanagement', '0008_auto_20170417_0938'),
    ]

    operations = [
        migrations.AlterField(
            model_name='link',
            name='url',
            field=models.CharField(max_length=1024),
        ),
    ]
