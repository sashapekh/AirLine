# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-06-06 21:48
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ticketapp', '0017_orderhotel_room_numbers'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReservationRoomInfo',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('room_type', models.CharField(max_length=100, null=True)),
                ('room_numbers', models.IntegerField(null=True)),
                ('person_number', models.IntegerField(null=True)),
                ('food_delivery', models.CharField(max_length=100, null=True)),
                ('start_date', models.DateField(null=True)),
                ('end_date', models.DateField(null=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='hotelroom',
            name='food',
        ),
        migrations.RemoveField(
            model_name='hotelroom',
            name='max_capacity',
        ),
        migrations.RemoveField(
            model_name='orderhotel',
            name='end_date',
        ),
        migrations.RemoveField(
            model_name='orderhotel',
            name='hotel_room_fk',
        ),
        migrations.RemoveField(
            model_name='orderhotel',
            name='room_numbers',
        ),
        migrations.RemoveField(
            model_name='orderhotel',
            name='start_date',
        ),
        migrations.AddField(
            model_name='orderhotel',
            name='reservation_room_fk',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='ticketapp.ReservationRoomInfo'),
        ),
    ]
