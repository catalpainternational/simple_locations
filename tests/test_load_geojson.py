import json

from django.db.models import QuerySet
from django.test import TestCase

from simple_locations.gis_functions import JsonFeature
from simple_locations.models import Area
from simple_locations.schemas import Feature, FeatureCollection
from tests.factories import AreaFactory  # type: ignore


class GeoJsonTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.area = AreaFactory()

    def test_geojson_queryset(self):
        json.loads(Area.geofunctions.all().to_geojson())

    def test_features(self):
        """
        Test the 'JSONObject' based manager which returns features
        """
        queryset: QuerySet[Area] = Area.objects.all()
        # Annotate a dict 'feature' to the queryset
        queryset = queryset.annotate(JsonFeature())

        # Assert that the "feature" is correctly a field on the queryset
        instance: Area = queryset.first()
        feature = getattr(instance, "feature", None)
        self.assertIsNotNone(feature)
        self.assertIsInstance(feature, dict)

        # Convert to a Pydantic 'feature' instance
        feature: Feature = Feature.parse_obj(feature)
        self.assertEqual(feature.type, "Feature")
        self.assertEqual(feature.geometry.type, "MultiPolygon")

    def test_feature_from_manager(self):
        """
        A shorter way of doing the same as above is to use
        the Manager instance on Area
        """
        for feature in Area.features.to_features():
            self.assertIsInstance(Feature.parse_obj(feature), Feature)

    def test_collection_from_manager(self):
        """
        A FeatureCollection should be returned from
        a QuerySet
        """
        for n in range(5):
            AreaFactory()
        fc = Area.features.to_featurecollection()
        self.assertIsInstance(fc, FeatureCollection)
