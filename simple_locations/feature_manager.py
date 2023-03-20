from django.db import models

from simple_locations.gis_functions import JsonFeature
from simple_locations.schemas import Feature, FeatureCollection


class FeatureQueryset(models.QuerySet):
    def to_featurecollection(self, simplify: float = 1e-3, quantize: int = 5) -> FeatureCollection:
        """
        GeoJSON Feature builder
        =======================

        >>> queryset = Area.geofunctions.all()
        >>> # Annotate a "feature" field on to the queryset
        >>> queryset.annotate(JsonFeature())
        >>> # Optional simplify, quantize the results:
        >>> queryset.annotate(JsonFeature(simplify=1e-3, quantize=5))
        >>> # Return an array for a FeatureCollection instance
        >>> queryset.aggregate(features = JSONBAgg(JsonFeature()))

        Pydantic integration
        ====================
        >>> from simple_locations.schemas import Feature
        >>> Feature.parse_obj(Area.geofunctions.all().annotate(JsonFeature()).first().feature)
        >>> # A list of features:
        >>> [Feature.parse_obj(i) for i in Area.geofunctions.filter(kind__name='district').to_features(simplify=1e-3, quantize=5).values_list('feature', flat=True)]
        >>> # A FeatureCollection:
        >>> FeatureCollection.parse_obj(queryset.aggregate(features = JSONBAgg(JsonFeature())))
        """
        return FeatureCollection.construct(features=[*self.to_features(simplify=simplify, quantize=quantize)])

    def annotate_features(self, simplify: float = 1e-3, quantize: int = 5):
        """
        Annotated 'feature' fields onto the queryset
        """
        return self.annotate(
            JsonFeature(
                simplify=simplify,
                quantize=quantize,
                # The following fields become "properties"
                id=models.F("id"),
                parent=models.F("parent"),
                code=models.F("code"),
                name=models.F("name"),
            )
        )

    def to_features(self, simplify: float = 1e-3, quantize: int = 5):
        """
        Generate features
        """
        return (
            Feature.construct(**area.feature) for area in self.annotate_features(simplify=simplify, quantize=quantize)
        )


class FeatureManager(models.Manager):
    def get_queryset(self):
        return FeatureQueryset(self.model, using=self._db)

    def to_features(self, simplify: float = 1e-3, quantize: int = 5):
        return self.get_queryset().to_features(simplify=simplify, quantize=quantize)

    def to_featurecollection(self, simplify: float = 1e-3, quantize: int = 5) -> FeatureCollection:
        return self.get_queryset().to_featurecollection(simplify=simplify, quantize=quantize)