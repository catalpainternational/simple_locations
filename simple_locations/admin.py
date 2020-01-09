#!/usr/bin/env python
# encoding=utf-8
# maintainer rgaudin

from django.conf import settings
from django.contrib.gis import admin
from django import forms

from mptt.admin import MPTTModelAdmin
from modeltranslation.admin import TranslationAdmin

from simple_locations.models import Point, AreaType, Area


class PointAdmin(admin.ModelAdmin):
    list_display = ('id', 'latitude', 'longitude')


class AreaTypeAdmin(TranslationAdmin):
    list_display = ('slug', 'name')


class AreaChildrenInline(admin.TabularInline):
    model = Area
    fields = ['name', 'code', 'kind']
    show_change_link = True
    extra = 0


class AreaAdmin(TranslationAdmin, MPTTModelAutocompleteAdmin, admin.OSMGeoAdmin):
    default_lon = getattr(settings, 'GIS_DEFAULT_LAT', -8.8742)
    default_lat = getattr(settings, 'GIS_DEFAULT_LON', 125.7275)
    default_zoom = 16
    map_template = "simple_locations/admin/osm.html"
    # debug = True  - enable if copy/pasting WKTs is useful
    units = 'km'
    list_display = ('name', 'kind', 'location', 'code')

class AreaAdmin(TranslationAdmin, MPTTModelAdmin):
    search_fields = ['code', 'name']
    list_filter = ('kind',)
    related_search_fields = {'parent': ('^name',)}
    inlines = [AreaChildrenInline]


admin.site.register(Point, PointAdmin)
admin.site.register(AreaType, AreaTypeAdmin)
admin.site.register(Area, AreaAdmin)
