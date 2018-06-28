#!/usr/bin/env python
# encoding=utf-8
# maintainer rgaudin

from django.contrib import admin
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


class AreaAdmin(MPTTModelAutocompleteAdmin):
    list_display = ( 'name', 'kind', 'location', 'code')
    search_fields = ['code', 'name']
    list_filter = ('kind',)
    related_search_fields = {'parent': ('^name',)}


admin.site.register(Point, PointAdmin)
admin.site.register(AreaType, AreaTypeAdmin)
admin.site.register(Area, AreaAdmin)
