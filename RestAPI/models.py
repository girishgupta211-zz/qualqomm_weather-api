# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from datetime import date

from django.db import models


class CityTemperature(models.Model):
    id = models.IntegerField(null=False, db_index=True, primary_key=True)
    temperature = models.CharField(max_length=500)
    location_lat = models.FloatField(null=False)
    location_lon = models.FloatField(null=False)
    location_city = models.CharField(max_length=50, null=False)
    location_state = models.CharField(max_length=50, null=False)
    date = models.DateField(default=date.today, null=False)

    class Meta:
        db_table = 'city_temperature'
