# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-06-06 15:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ticketapp', '0016_auto_20170606_1230'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderhotel',
            name='room_numbers',
            field=models.IntegerField(default=1),
        ),
    ]
