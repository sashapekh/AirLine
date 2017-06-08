# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-06-06 12:30
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ticketapp', '0015_auto_20170606_1213'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderhotel',
            name='hotel_room_fk',
            field=models.ForeignKey(default=3, on_delete=django.db.models.deletion.CASCADE, to='ticketapp.HotelRoom'),
        ),
        migrations.AlterField(
            model_name='hotelroom',
            name='hotel_fk',
            field=models.ForeignKey(default=3, on_delete=django.db.models.deletion.CASCADE, to='ticketapp.Hotel'),
        ),
        migrations.AlterField(
            model_name='hotelroom',
            name='max_capacity',
            field=models.IntegerField(default=1),
        ),
    ]