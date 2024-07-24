from django.contrib.gis.db import models

from simple_locations.base_area import AbstractBaseArea


class WgsPoint(models.Model):
    position = models.PointField(srid=4326)


class MercatorPoint(models.Model):
    position = models.PointField(srid=3857)

class ConfiguredAreaModel(AbstractBaseArea):
    extra_field = models.CharField(max_length=30)
    extra_field2 = models.CharField(max_length=30, default='')