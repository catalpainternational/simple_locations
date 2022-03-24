from django.contrib.gis.geos import Point
from django.test import TestCase

from simple_locations.models import Area, intersects_areas
from sl_tests.models import WgsPoint
from tests.factories import AreaFactory, WgsPointFactory


class IntersectsAreaTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.area = AreaFactory()
        cls.point = WgsPointFactory()
        cls.point_outside_area = WgsPointFactory(position=Point(5, 5))

    def test_filter_area(self):
        self.assertEqual(Area.objects.count(), 1)
        self.assertEqual(WgsPoint.objects.count(), 2)
        filtered_points = WgsPoint.objects.extra(
            **intersects_areas(Area.objects.all().values_list("id", flat=True), WgsPoint)
        )
        self.assertEqual(filtered_points.count(), 1)
