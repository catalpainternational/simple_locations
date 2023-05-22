from typing import List, Optional, TypeVar, Union

# We import this and then cast to JSON in the db. The default function returns text.
from django.contrib.gis.db.models.functions import AsGeoJSON as AsGeoJson_
from django.db import models
from django.db.models import F, Func, Value
from django.db.models.fields.json import JSONField
from django.db.models.functions.comparison import JSONObject


class Quantize(models.Func):
    """
    ST_QuantizeCoordinates determines the number of bits (N)
    required to represent a coordinate value with a specified number
    of digits after the decimal point, and then sets all but the N
    most significant bits to zero. The resulting coordinate value will
    still round to the original value, but will have improved compressiblity
    """

    function = "ST_QuantizeCoordinates"
    template = "%(function)s(%(expressions)s, %(quantize)s)"


class Simplify(models.Func):
    """
    Returns a "simplified" version of the given geometry using the Douglas-Peucker algorithm.
    """

    function = "ST_SIMPLIFY"
    template = "%(function)s(%(expressions)s, %(simplify)s)"


class SimplifyPreserve(Simplify):
    """
    Returns a "simplified" version of the given geometry using the Douglas-Peucker algorithm.
    """

    function = "ST_SIMPLIFYPRESERVETOPOLOGY"
    template = "%(function)s(%(expressions)s, %(simplify)s)"


class Multi(models.Func):
    """
    Returns the geometry as a MULTI* geometry collection.
    If the geometry is already a collection, it is returned unchanged.
    """

    function = "ST_Multi"


M = TypeVar("M", bound=models.Model)


class AsGeoJson(AsGeoJson_):
    """
    Official Django function returns text. This wraps that in a JSON cast
    and tells Python to expect a JSONField
    """

    ...
    template = f"{AsGeoJson_.template}::json"
    # output_field = models.JSONField()


class JsonFeature(models.Func):
    """
    Modern (Django 3.2+) GeoJSON object simplifier and serializer
    """

    function = "JSONB_BUILD_OBJECT"
    output_field = JSONField()
    default_alias = "feature"
    maxdecimaldigits = 6

    def __init__(
        self,
        # These are optional geometry processing functions which affect the
        # geometry before it's converted to GeoJSON
        geom_field: str = "geom",
        simplify: Optional[float] = None,
        quantize: Optional[int] = None,
        multi: Optional[bool] = False,
        # Include the Primary Key as ID for the model?
        # Primary key will be cast to an int or string, if possible
        include_id_field: Optional[bool] = True,
        # Additional fields for "ST_AsGeoJson"
        # include bbox, crs, precision
        # These are sufffixed with `_` to distinguish them from `fields`
        bbox_: bool = False,
        crs_: bool = False,
        precision_: int = 6,
        # Properties ('fields' or 'annotations' on the model)
        # which will become part of the GIS "properties" dict
        **fields,
    ):
        expressions: List[Union[Value, F, Func]] = []
        if include_id_field:
            expressions.extend((Value("id"), models.F("pk")))
        g: Union[F, Func] = models.F(geom_field)
        if simplify:
            g = SimplifyPreserve(g, simplify=simplify)
        if quantize:
            g = Quantize(g, quantize=quantize)
        if multi:
            g = Multi(g)
        expressions.extend((Value("type"), Value("Feature")))
        expressions.extend((Value("geometry"), AsGeoJson(g, bbox=bbox_, crs=crs_, precision=precision_)))
        expressions.extend((Value("properties"), JSONObject(**fields)))
        super().__init__(*expressions)
