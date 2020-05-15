#!/usr/bin/env python
# encoding=utf-8
# vim: ai ts=4 sts=4 et sw=4


from django.contrib.gis.db.models import MultiPolygonField
from django.db import models
from django.utils.translation import ugettext as _, ugettext_lazy as __
# from code_generator.fields import CodeField # removed so that we can use
# South
from mptt.models import MPTTModel

class Point(models.Model):

    class Meta:
        verbose_name = __("Point")
        verbose_name_plural = __("Points")
        app_label = 'simple_locations'

    latitude = models.DecimalField(max_digits=13, decimal_places=10)
    longitude = models.DecimalField(max_digits=13, decimal_places=10)

    def __str__(self):
        return _(u"%(lat)s, %(lon)s") % {'lat': self.latitude,
                                         'lon': self.longitude}


class AreaType(models.Model):

    class Meta:
        verbose_name = __("Area Type")
        verbose_name_plural = __("Area Types")
        app_label = 'simple_locations'

    name = models.CharField(max_length=100)
    slug = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return _(self.name)


class Area(MPTTModel):

    class Meta:
        unique_together = ('code', 'kind')
        verbose_name = __("Area")
        verbose_name_plural = __("Areas")
        app_label = 'simple_locations'

    class MPTTMeta:
        parent_attr = 'parent'
        order_insertion_by = ['name']

    name = models.CharField(max_length=100)
    code = models.CharField(max_length=50,)  # was CodeField
    kind = models.ForeignKey('AreaType', blank=True, null=True, on_delete=models.CASCADE)
    location = models.ForeignKey(Point, blank=True, null=True, on_delete=models.CASCADE)
    geom = MultiPolygonField(srid=4326, blank=True, null=True)
    parent = models.ForeignKey('self', blank=True, null=True, related_name='children', on_delete=models.CASCADE)

    def delete(self):
        super(Area, self).delete()

    def get_ancestor_at_level(self, level=2):
        """Get the area ancestor at a given level

        Will travel the tree until it reaches the level or return self if already under that level"""
        if self.get_level() <= level:
            return self
        return self.get_ancestors()[level]

    def display_name_and_type(self):
        '''Area name and type

        Example District of Bamako'''
        return u"%(type)s of %(area)s" % {'type': self.kind.name, 'area': self.name}

    def display_with_parent(self):
        '''Print Area name and kind and parent name and kind

        Example: Aldeia of Baha-Neo in Suco of Lia Ruca'''
        if not self.parent:
            return self.display_name_and_type()
        elif self.kind.name == 'District':
            return self.display_name_and_type()
        else:
            return u"%(this)s in %(parent)s" % \
                {
                    'this': self.display_name_and_type(),
                    'parent': self.parent.display_name_and_type()
                }

    def __str__(self):
        ''' print Area name from its Kind and parent

        Example: Bamako '''

        # don't add-in kind if kind name is already part of name.
        # if (not self.parent) or (not self.kind) or self.name.startswith(self.kind.name):
        #    return self.name
        # else:
        #    return _(u"%(type)s of %(area)s.") % {'type': self.kind.name, \
        #                                              'area': self.name,}

        return self.name
