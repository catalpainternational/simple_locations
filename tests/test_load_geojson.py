
import json
from django.test import TestCase

from tests.factories import AreaFactory

from simple_locations.models import Area


class GeoJsonTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.area = AreaFactory()

    def test_geojson_queryset(self):
        json.loads(Area.geofunctions.all().to_geojson())
