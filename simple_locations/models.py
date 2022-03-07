from django.contrib.gis.db.models import LineStringField, MultiPolygonField
from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.utils.translation import gettext as _
from django.utils.translation import gettext_lazy as __
from mptt.models import MPTTModel


class DateStampedModel(models.Model):
    date_created = models.DateField(verbose_name=_("Date Created"), auto_now_add=True, null=True, blank=True)
    date_modified = models.DateField(verbose_name=_("Last Modified"), null=True, blank=True)

    class Meta:
        abstract = True


class Point(models.Model):
    class Meta:
        verbose_name = __("Point")
        verbose_name_plural = __("Points")
        app_label = "simple_locations"

    latitude = models.DecimalField(max_digits=13, decimal_places=10)
    longitude = models.DecimalField(max_digits=13, decimal_places=10)

    def __str__(self):
        return _("%(lat)s, %(lon)s") % {"lat": self.latitude, "lon": self.longitude}


class AreaType(models.Model):
    class Meta:
        verbose_name = __("Area Type")
        verbose_name_plural = __("Area Types")
        app_label = "simple_locations"

    name = models.CharField(max_length=100)
    slug = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return _(self.name)


class Area(MPTTModel):
    class Meta:
        unique_together = ("code", "kind")
        verbose_name = __("Area")
        verbose_name_plural = __("Areas")
        app_label = "simple_locations"

    class MPTTMeta:
        parent_attr = "parent"
        order_insertion_by = ["name"]

    name = models.CharField(max_length=100)
    code = models.CharField(max_length=50, unique=True)  # was CodeField
    kind = models.ForeignKey("AreaType", blank=True, null=True, on_delete=models.CASCADE)
    location = models.ForeignKey(Point, blank=True, null=True, on_delete=models.CASCADE)
    geom = MultiPolygonField(srid=4326, blank=True, null=True)
    parent = models.ForeignKey("self", blank=True, null=True, related_name="children", on_delete=models.CASCADE)

    def delete(self):
        super(Area, self).delete()

    def get_ancestor_at_level(self, level=2) -> "Area":
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
        """print Area name from its Kind and parent

        Example: Bamako"""

        # don't add-in kind if kind name is already part of name.
        # if (not self.parent) or (not self.kind) or self.name.startswith(self.kind.name):
        #    return self.name
        # else:
        #    return _(u"%(type)s of %(area)s.") % {'type': self.kind.name, \
        #                                              'area': self.name,}

        return self.name


class ProjectedArea(models.Model):
    """
    Projected "area" instances in the common web mercator (3857)
    This allows for correctly indexed spatial queries against data which is
    in that coordinates system when ingested.
    Most commonly this would be OSM data
    """

    geom = MultiPolygonField(null=True, blank=True, srid=3857)
    area = models.OneToOneField("Area", primary_key=True, on_delete=models.CASCADE)


class Border(models.Model):
    """
    Shared parts of border topologies are referenced
    here in order to make a more efficient mapping layer.
    When we do this we can greatly reduce the amount of data
    sent to client (for PNG 'area' is 9.6M on-disk, 'lines' is 2.3M on-disk)
    """

    # srid could be 4326 or 3857. 3857 is easier for simplification
    # because it's in meters; simplification in degrees is not fun.
    geom = LineStringField(srid=3857)
    area = models.ManyToManyField("Area")

    # The following fields are denormalised in order to
    # simplify generting and filtering vector data
    area_ids = ArrayField(models.IntegerField(), default=list)
    area_types = ArrayField(models.IntegerField(), default=list)


class AreaProfile(DateStampedModel):
    area = models.OneToOneField("Area", on_delete=models.CASCADE, primary_key=True)
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

    area = models.ForeignKey("Area", on_delete=models.CASCADE)
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
