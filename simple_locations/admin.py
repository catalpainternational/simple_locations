#!/usr/bin/env python
# encoding=utf-8
# maintainer rgaudin

from django.conf import settings
from django.contrib.gis import admin
from django import forms

from mptt.admin import MPTTModelAdmin

from simple_locations.models import Point, AreaType, Area

try:
    # optionally use django_extensions' ForeignKeyAutocompleteAdmin if available
    from django_extensions.admin import ForeignKeyAutocompleteAdmin
    class MPTTModelAutocompleteAdmin(MPTTModelAdmin, ForeignKeyAutocompleteAdmin):
        pass
except ImportError:
    class MPTTModelAutocompleteAdmin(MPTTModelAdmin):
        pass


class PointAdmin(admin.ModelAdmin):
    list_display = ('id', 'latitude', 'longitude')


class AreaTypeAdmin(admin.ModelAdmin):
    list_display = ('slug', 'name')


class AreadChildrenInline(admin.TabularInline):
    model = Area
    fields = ['name', 'code', 'kind']
    show_change_link = True
    extra = 0


class AreaAdmin(MPTTModelAutocompleteAdmin, admin.OSMGeoAdmin):
    # default_lon = getattr(settings, 'GIS_DEFAULT_LAT', -8.8742)
    # default_lat = getattr(settings, 'GIS_DEFAULT_LON', 125.7275)
    default_lon = -8.8742
    default_lat = 125.7275
    default_zoom = 16
    # debug = True  - enable if copy/pasting WKTs is useful
    units = 'km'
    list_display = ('name', 'kind', 'location', 'code')
    search_fields = ['code', 'name']
    list_filter = ('kind',)
    related_search_fields = {'parent': ('^name',)}
    inlines = [AreadChildrenInline]


admin.site.register(Point, PointAdmin)
admin.site.register(AreaType, AreaTypeAdmin)
admin.site.register(Area, AreaAdmin)
