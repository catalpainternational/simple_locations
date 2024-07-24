from django.db import models

from django.contrib.gis.db.models import LineStringField, MultiPolygonField
from django.contrib.postgres.fields import ArrayField

from mptt.models import MPTTModel
from simple_locations.feature_manager import FeatureQueryset
from simple_locations.manager import AreaQueryset
from django.utils.translation import gettext as _
from django.utils.translation import gettext_lazy as __


class AbstractBaseAreaType(models.Model):
    class Meta:
        verbose_name = __("Area Type")
        verbose_name_plural = __("Area Types")
        abstract = True

    name = models.CharField(max_length=100)
    slug = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return _(self.name)


class AbstractBasePoint(models.Model):
    class Meta:
        verbose_name = __("Point")
        verbose_name_plural = __("Points")
        abstract = True

    latitude = models.DecimalField(max_digits=13, decimal_places=10)
    longitude = models.DecimalField(max_digits=13, decimal_places=10)

    def __str__(self):
        return _("%(lat)s, %(lon)s") % {"lat": self.latitude, "lon": self.longitude}

Meta = type('Meta', (object,), {'abstract': True})

def get_area_base(kind_model: AbstractBaseAreaType, point_model: AbstractBasePoint):
    """Return the AbstractBaseArea base class
        kind_model: Concrete Model for Area Type
        point_model: Concrete Model for Point
    """
    attrs = {
        'kind': models.ForeignKey(kind_model, blank=True, null=True, on_delete=models.CASCADE),
        'location': models.ForeignKey(point_model, blank=True, null=True, on_delete=models.CASCADE),
        '__module__': __name__,
        'Meta': Meta(),
    }
    return type('AbstractBaseArea', (_AbstractBaseArea,), attrs)

class _AbstractBaseArea(MPTTModel):
    class Meta:
        unique_together = ("code", "kind")
        verbose_name = __("Area")
        verbose_name_plural = __("Areas")
        abstract = True

    class MPTTMeta:
        parent_attr = "parent"
        order_insertion_by = ["name"]

    @classmethod
    def kind(cls):
        return cls.kind_model

    name = models.CharField(max_length=100)
    code = models.CharField(max_length=50, unique=True)  # was CodeField
    geom = MultiPolygonField(srid=4326, blank=True, null=True)
    parent = models.ForeignKey("self", blank=True, null=True, related_name="children", on_delete=models.CASCADE)

    def delete(self):
        super().delete()

    def get_ancestor_at_level(self, level=2) -> "AbstractBaseArea":
        """Get the area ancestor at a given level

        Will travel the tree until it reaches the level or return self if already under that level"""
        if self.get_level() <= level:
            return self
        return self.get_ancestors()[level]

    def display_name_and_type(self) -> str:
        """Area name and type

        Example District of Bamako"""
        return f"{self.kind.name} of {self.name}"

    def display_with_parent(self) -> str:
        """Print Area name and kind and parent name and kind

        Example: Aldeia of Baha-Neo in Suco of Lia Ruca"""
        if not self.parent:
            return self.display_name_and_type()
        elif self.kind.name == "District":
            return self.display_name_and_type()
        else:
            return "%(this)s in %(parent)s" % {
                "this": self.display_name_and_type(),
                "parent": self.parent.display_name_and_type(),
            }

    def __str__(self) -> str:
        return self.name

    geofunctions = AreaQueryset.as_manager()
    features = FeatureQueryset.as_manager()


def get_projected_area_base(area_model: _AbstractBaseArea):
    """Return the AbstractBaseProjectedArea base class
        area_model: Concrete Model for Area
    """
    attrs = {
        'area': models.OneToOneField(area_model, primary_key=True, on_delete=models.CASCADE),
        '__module__': __name__,
        'Meta': Meta(),
    }
    return type('AbstractBaseProjectedArea', (_AbstractBaseProjectedArea,), attrs)

class _AbstractBaseProjectedArea(models.Model):
    """
    Projected "area" instances in the common web mercator (3857)
    This allows for correctly indexed spatial queries against data which is
    in that coordinates system when ingested.
    Most commonly this would be OSM data
    """

    class Meta:
        abstract = True

    geom = MultiPolygonField(null=True, blank=True, srid=3857)

def get_border_base(area_model: _AbstractBaseArea):
    """Return the AbstractBaseProjectedArea base class
        area_model: Concrete Model for Area
    """
    attrs = {
        'area': models.ManyToManyField(area_model),
        '__module__': __name__,
        'Meta': Meta(),
    }
    return type('AbstractBaseBorder', (_AbstractBaseBorder,), attrs)

class _AbstractBaseBorder(models.Model):
    """
    Shared parts of border topologies are referenced
    here in order to make a more efficient mapping layer.
    When we do this we can greatly reduce the amount of data
    sent to client (for PNG 'area' is 9.6M on-disk, 'lines' is 2.3M on-disk)
    """

    class Meta:
        abstract = True

    # srid could be 4326 or 3857. 3857 is easier for simplification
    # because it's in meters; simplification in degrees is not fun.
    geom = LineStringField(srid=3857)

    # The following fields are denormalised in order to
    # simplify generting and filtering vector data
    area_ids = ArrayField(models.IntegerField(), default=list)
    area_types = ArrayField(models.IntegerField(), default=list)
