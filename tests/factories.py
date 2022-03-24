import factory
import factory.fuzzy
from django.contrib.gis.geos import MultiPolygon, Point, Polygon
from factory.django import DjangoModelFactory

from simple_locations.models import Area, AreaType
from sl_tests.models import WgsPoint


class AreaTypeFactory(DjangoModelFactory):
    class Meta:
        model = AreaType
        django_get_or_create = ("name",)

    name = factory.fuzzy.FuzzyText()
    slug = factory.fuzzy.FuzzyText()


class AreaFactory(DjangoModelFactory):
    class Meta:
        model = Area
        django_get_or_create = ("code",)

    code = factory.fuzzy.FuzzyText()
    name = factory.fuzzy.FuzzyText()
    kind = factory.SubFactory(AreaTypeFactory)
    geom = MultiPolygon(Polygon(((0, 0), (0, 1), (1, 1), (0, 0))), Polygon(((1, 1), (1, 2), (2, 2), (1, 1))))


class ProjectedAreaFactory(DjangoModelFactory):
    class Meta:
        model = Area
        django_get_or_create = ("code",)

    area = factory.SubFactory(AreaFactory)
    geom = MultiPolygon(Polygon(((0, 0), (0, 1), (1, 1), (0, 0))), Polygon(((1, 1), (1, 2), (2, 2), (1, 1))))


class WgsPointFactory(DjangoModelFactory):
    class Meta:
        model = WgsPoint

    position = Point(0.1, 0.1)
