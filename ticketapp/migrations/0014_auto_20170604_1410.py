# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-06-04 14:10
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ticketapp', '0013_auto_20170604_1020'),
    ]

    operations = [
        migrations.RenameField(
            model_name='hotel',
            old_name='h_starts',
            new_name='h_stars',
        ),
    ]
