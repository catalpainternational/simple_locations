#!/usr/bin/env python
# encoding=utf-8
# maintainer rgaudin

from django.contrib import admin
from django import forms
from mptt.admin import MPTTModelAdmin

from models import Point, AreaType, Area, Facility, FacilityType
from mptt.admin import MPTTChangeList
from catalpa.lib.autocomplete_admin import FkAutocompleteAdmin
class PointAdmin(admin.ModelAdmin):
    list_display = ('id', 'latitude', 'longitude')


class AreaTypeAdmin(admin.ModelAdmin):
    list_display = ('slug', 'name')


class AreaAdmin(MPTTModelAdmin):
    list_display = ( 'name', 'kind', 'location', 'code')
    search_fields = ['code', 'name']
    list_filter = ('kind',)



class FacilityTypeAdmin(admin.ModelAdmin):
    model = FacilityType


class FacilityAdmin(FkAutocompleteAdmin):
    model = Facility
    fields = ['name', 'code', 'type', 'area', 'parent',]
    list_filter = ('type',)
    search_fields = ['name',]
    related_search_fields = {'area': ('^name',),
                             'parent': ('^name',),}
    

admin.site.register(Point, PointAdmin)
admin.site.register(AreaType, AreaTypeAdmin)
admin.site.register(Area, AreaAdmin)
admin.site.register(Facility, FacilityAdmin)
admin.site.register(FacilityType, FacilityTypeAdmin)
