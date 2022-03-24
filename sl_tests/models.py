from django.contrib.gis.db import models


class WgsPoint(models.Model):
    position = models.PointField(srid=4326)


class MercatorPoint(models.Model):
    position = models.PointField(srid=3857)
