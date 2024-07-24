from typing import Iterable, List, Optional, Type

from django.contrib.gis.db.models import (
    GeometryField,
)
from django.db import models
from django.utils.translation import gettext as _
from django.utils.translation import gettext_lazy as __

from . import base_models


def get_geom_field(model) -> GeometryField:
    """
    Returns the first field likely to be a geometry field
    from a model
    """
    fields = model._meta.fields  # type: List
    for field_ in fields:
        if isinstance(field_, GeometryField):
            return field_
    raise KeyError(f"No geometry field could be identified for {model}")


def intersects_areas(area_ids: Iterable[int], model: models.Model, geom_field: Optional[str] = None):
    """
    Return parameters for an 'extra' clause intersecting an area
    This function uses SRID 3857 and the corresponding projected areas
    for compatibility with osm import

    This example - from DIRD's location profile airstrips:

    >>> extra_clause = intersects_areas(Area.objects.values_list('id', flat=True), Airstrip)
    >>> Airstrip.objects.extra(**extra_clause, Airstrip)

    """

    def _area_model(srid: int) -> Type[models.Model]:
        """
        Determine which model to apply the intersection to
        based on the SRID
        """
        if srid == 4326:
            return Area
        elif srid == 3857:
            return ProjectedArea
        raise AssertionError("Unhandled SRID")

    geom_field_instance = model._meta.get_field(geom_field) if geom_field else get_geom_field(model)

    if not isinstance(geom_field_instance, GeometryField):
        raise TypeError

    geom_field_name: str = geom_field_instance.db_column or geom_field_instance.attname

    area_query_values = ",".join(map(str, area_ids))
    area_clause = f"""ANY ('{{{area_query_values}}}'::int[])"""

    area_model = _area_model(geom_field_instance.srid)
    area_table_name = area_model._meta.db_table
    area_table_pk = area_model._meta.pk.db_column or area_model._meta.pk.attname

    return dict(
        tables=[area_table_name],
        where=[
            f'"{area_table_name}"."{area_table_pk}" = {area_clause}',
            f'ST_INTERSECTS("{area_table_name}"."geom", "{model._meta.db_table}"."{geom_field_name}")',
        ],
    )


class DateStampedModel(models.Model):
    date_created = models.DateField(verbose_name=_("Date Created"), auto_now_add=True, null=True, blank=True)
    date_modified = models.DateField(verbose_name=_("Last Modified"), null=True, blank=True)

    class Meta:
        abstract = True


class Point(base_models.AbstractBasePoint):
    class Meta(base_models.AbstractBasePoint.Meta):
        app_label = "simple_locations"

class AreaType(base_models.AbstractBaseAreaType):
    class Meta(base_models.AbstractBaseAreaType.Meta):
        app_label = "simple_locations"

class Area(base_models.get_area_base(AreaType, Point)):

    class Meta(base_models._AbstractBaseArea.Meta):
        app_label = "simple_locations"

class ProjectedArea(base_models.get_projected_area_base(Area)):
    pass


class Border(base_models.get_border_base(Area)):
    pass


class AreaProfile(DateStampedModel):
    area = models.OneToOneField(Area, on_delete=models.CASCADE, primary_key=True)
    description = models.TextField()


class IndicatorMeasureSchema(models.Model):
    """
    Declare the "shape" of the data to be displayed.
    See :
    https://pypi.org/project/jsonschema/
    https://json-schema.org/
    """

    schema = models.TextField()


class AreaIndicator(DateStampedModel):
    """
    Initially required for PNG DIMS
    """

    class IndicatorMeasureChoice(models.TextChoices):
        """
        Derived from the IATI standard, this determines the "type" of
        data which is being measured - is it percentage, count, or on some sort of scale?
        """

        UNIT = "U", _("Units")
        PERCENTAGE = "P", _("Percentages")
        NOMINAL = "N", _("Nominal")
        ORDINAL = "O", _("Ordinal")
        QUALITATIVE = "Q", _("Qualitative")

    area = models.ForeignKey(Area, on_delete=models.CASCADE)
    name = models.TextField()

    measure = models.CharField(
        max_length=2,
        choices=IndicatorMeasureChoice.choices,
        default=IndicatorMeasureChoice.UNIT,
        help_text=_("Define the unit of measure in which the value is reported."),
    )

    # In order to permit for instance a time-series-keyed mesaurement,
    # this is a JSON field rather than a text field
    value = models.JSONField()

    # Define parameters for the measurement.
    # For example: {Gender: "Male", age_range: [0,16], is_smoker: no}
    dimensions = models.JSONField(help_text=_("A category used for disaggregating the result by gender, age, etc."))
