# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-06-04 14:37
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('site1', '0019_auto_20160604_1145'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='company',
            new_name='organization',
        ),
        migrations.RenameField(
            model_name='devices',
            old_name='company',
            new_name='organization',
        ),
        migrations.RenameField(
            model_name='employee',
            old_name='company',
            new_name='organization',
        ),
    ]
