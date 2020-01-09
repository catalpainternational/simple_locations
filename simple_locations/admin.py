#!/usr/bin/env python
# encoding=utf-8
# maintainer rgaudin

from django.contrib import admin

from mptt.admin import MPTTModelAdmin
from modeltranslation.admin import TranslationAdmin

from simple_locations.models import Point, AreaType, Area


class PointAdmin(admin.ModelAdmin):
    list_display = ('id', 'latitude', 'longitude')


class AreaTypeAdmin(TranslationAdmin):
    list_display = ('slug', 'name')


class AreaAdmin(TranslationAdmin, MPTTModelAdmin):
    list_display = ('name', 'kind', 'location', 'code')
    search_fields = ['code', 'name']
    list_filter = ('kind',)
    related_search_fields = {'parent': ('^name',)}


admin.site.register(Point, PointAdmin)
admin.site.register(AreaType, AreaTypeAdmin)
admin.site.register(Area, AreaAdmin)
