# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-03 13:27
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ATA_box',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone', models.DecimalField(decimal_places=0, max_digits=11)),
                ('mac', models.CharField(max_length=23)),
                ('status', models.CharField(max_length=1)),
                ('last_online', models.DateTimeField()),
                ('fw_version', models.CharField(max_length=23)),
            ],
        ),
    ]
