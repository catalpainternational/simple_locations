from datetime import date
from decimal import Decimal
from typing import Any, Optional

from django.db import models
from mptt.models import MPTTModel

from simple_locations.feature_manager import FeatureQueryset

class DateStampedModel(models.Model):
    date_created: date
    date_modified: date

    class Meta:
        abstract: bool

class Point(models.Model):
    class Meta:
        verbose_name: str
        verbose_name_plural: str
        app_label: str
    latitude: Decimal
    longitude: Decimal

class AreaType(models.Model):
    class Meta:
        verbose_name: str
        verbose_name_plural: str
        app_label: str
    name: Any
    slug: Any

class Area(MPTTModel):
    class Meta:
        unique_together: bool
        verbose_name: str
        verbose_name_plural: str
        app_label: str

    class MPTTMeta:
        parent_attr: str
        order_insertion_by: Any
    name: str
    code: str
    kind: AreaType
    kind_id: Optional[int]
    location: Optional[Point]
    location_id: Optional[int]
    geom: Any
    parent: Area
    parent_id: int
    def delete(self) -> None: ...
    def get_ancestor_at_level(self, level: int = ...) -> Area: ...
    def display_name_and_type(self): ...
    def display_with_parent(self): ...
    features: FeatureQueryset

class AreaProfile(DateStampedModel):
    area: Any
    description: Any

class IndicatorMeasureSchema(models.Model):
    schema: Any

class AreaIndicator(DateStampedModel):
    class IndicatorMeasureChoice(models.TextChoices):
        UNIT: Any
        PERCENTAGE: Any
        NOMINAL: Any
        ORDINAL: Any
        QUALITATIVE: Any
    area: Any
    name: Any
    measure: Any
    value: Any
    dimensions: Any
