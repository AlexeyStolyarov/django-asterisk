# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-05-29 06:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('site1', '0010_auto_20160528_1313'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ata_box',
            name='mac',
            field=models.CharField(default=0, max_length=12),
            preserve_default=False,
        ),
    ]
