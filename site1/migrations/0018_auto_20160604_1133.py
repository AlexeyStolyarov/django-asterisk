# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-06-04 11:33
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('site1', '0017_auto_20160604_0918'),
    ]

    operations = [
        migrations.RenameField(
            model_name='devices',
            old_name='companyid',
            new_name='company',
        ),
    ]
