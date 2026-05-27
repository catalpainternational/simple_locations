import json

import pytest
from django.test import TestCase

from simple_locations.models import Area
from tests.factories import AreaFactory  # type: ignore

pytestmark = pytest.mark.django_db


class GeoJsonTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.area = AreaFactory()

    def test_geojson_queryset(self):
        json.loads(Area.geofunctions.all().to_geojson())
