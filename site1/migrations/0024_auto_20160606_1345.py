# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-06-06 13:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('site1', '0023_auto_20160606_1211'),
    ]

    operations = [
        migrations.AddField(
            model_name='device',
            name='sip_control_registered',
            field=models.CharField(blank=True, max_length=6, null=True),
        ),
        migrations.AddField(
            model_name='device',
            name='sip_voip_registered',
            field=models.CharField(blank=True, max_length=6, null=True),
        ),
    ]
