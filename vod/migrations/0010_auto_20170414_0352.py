# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-04-14 03:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vod', '0009_auto_20170414_0338'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='description',
            field=models.TextField(),
        ),
    ]
