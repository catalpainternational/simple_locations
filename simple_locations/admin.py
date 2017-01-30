#!/usr/bin/env python
# encoding=utf-8
# maintainer rgaudin

from django.contrib import admin
from django import forms

from mptt.admin import MPTTModelAdmin

from simple_locations.models import Point, AreaType, Area


class PointAdmin(admin.ModelAdmin):
    list_display = ('id', 'latitude', 'longitude')


class AreaTypeAdmin(admin.ModelAdmin):
    list_display = ('slug', 'name')


class AreaAdmin(MPTTModelAdmin):
    list_display = ( 'name', 'kind', 'location', 'code')
    search_fields = ['code', 'name']
    list_filter = ('kind',)
    

admin.site.register(Point, PointAdmin)
admin.site.register(AreaType, AreaTypeAdmin)
admin.site.register(Area, AreaAdmin)
