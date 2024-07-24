from django.db import models

from django.contrib.gis.db.models import MultiPolygonField

from mptt.models import MPTTModel
from simple_locations.feature_manager import FeatureQueryset
from simple_locations.manager import AreaQueryset
from django.utils.translation import gettext_lazy as __


class AbstractBaseArea(MPTTModel):
    class Meta:
        unique_together = ("code", "kind")
        verbose_name = __("Area")
        verbose_name_plural = __("Areas")
        abstract = True

    class MPTTMeta:
        parent_attr = "parent"
        order_insertion_by = ["name"]

    name = models.CharField(max_length=100)
    code = models.CharField(max_length=50, unique=True)  # was CodeField
    kind = models.ForeignKey("simple_locations.AreaType", blank=True, null=True, on_delete=models.CASCADE)
    location = models.ForeignKey("simple_locations.Point", blank=True, null=True, on_delete=models.CASCADE)
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