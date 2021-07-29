from django.conf import settings
from django.contrib.gis import admin
from mptt.admin import MPTTModelAdmin

from simple_locations.models import Area, AreaIndicator, AreaType, Point

area_admin_classes = [admin.OSMGeoAdmin, MPTTModelAdmin]

# Translated models are "nice to have"
try:
    from modeltranslation.admin import TranslationAdmin

    area_admin_classes.append(TranslationAdmin)
    area_type_admin = TranslationAdmin
except ImportError:
    TranslationAdmin = admin.ModelAdmin
    pass


class PointAdmin(admin.ModelAdmin):
    list_display = ("id", "latitude", "longitude")


class AreaTypeAdmin(TranslationAdmin):
    list_display = ("slug", "name")


class AreaChildrenInline(admin.TabularInline):
    model = Area
    fields = ["name", "code", "kind"]
    show_change_link = True
    extra = 0


area_admin_settings = {
    "default_lon": getattr(settings, "GIS_DEFAULT_LAT", -8.8742),
    "default_lat": getattr(settings, "GIS_DEFAULT_LON", 125.7275),
    "default_zoom": 16,
    "map_template": "simple_locations/admin/osm.html",
    # "debug": True  - enable if copy/pasting WKTs is useful,
    "units": "km",
    "list_display": ("name", "kind", "location", "code"),
    "search_fields": ["code", "name"],
    "list_filter": ("kind",),
    "related_search_fields": {"parent": ("^name",)},
    "inlines": [AreaChildrenInline],
}

AreaAdminClass = type("AreaAdminClass", tuple(area_admin_classes), area_admin_settings)

admin.site.register(Point, PointAdmin)
admin.site.register(AreaType, AreaTypeAdmin)
admin.site.register(Area, AreaAdminClass)
admin.site.register(AreaIndicator)
