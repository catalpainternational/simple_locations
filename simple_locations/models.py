#!/usr/bin/env python
# encoding=utf-8
# vim: ai ts=4 sts=4 et sw=4

import uuid

from django.db import models
from django.utils.translation import ugettext as _, ugettext_lazy as __
# from code_generator.fields import CodeField # removed so that we can use
# South
import mptt
from mptt.models import MPTTModel


try:
    from mptt.models import MPTTModel
except ImportError:
    # django-mptt < 0.4
    MPTTModel = models.Model


class Point(models.Model):

    class Meta:
        verbose_name = __("Point")
        verbose_name_plural = __("Points")

    latitude = models.DecimalField(max_digits=13, decimal_places=10)
    longitude = models.DecimalField(max_digits=13, decimal_places=10)

    def __unicode__(self):
        return _(u"%(lat)s, %(lon)s") % {'lat': self.latitude,
                                         'lon': self.longitude}


class AreaType(models.Model):

    class Meta:
        verbose_name = __("Area Type")
        verbose_name_plural = __("Area Types")

    name = models.CharField(max_length=100)
    slug = models.CharField(max_length=30, unique=True)

    def __unicode__(self):
        return _(self.name)


class Area(MPTTModel):

    class Meta:
        unique_together = ('code', 'kind')
        verbose_name = __("Area")
        verbose_name_plural = __("Areas")

    class MPTTMeta:
        parent_attr = 'parent'
        order_insertion_by = ['name']

    name = models.CharField(max_length=100)
    code = models.CharField(max_length=50,)  # was CodeField
    kind = models.ForeignKey('AreaType', blank=True, null=True)
    location = models.ForeignKey(Point, blank=True, null=True)
    parent = models.ForeignKey('self', blank=True, null=True,
                               related_name='children')

    def delete(self):
        super(Area, self).delete()

    def display_name_and_type(self):
        '''Area name and type

Example District of Bamako'''
        return u"%(type)s of %(area)s" % {'type': self.kind.name, 'area': self.name}

    def display_with_parent(self):
        ''' print Area name and kind and parent name and kind

Example: District of Bamako in '''
        if not self.parent:
            return self.display_name_and_type()
        else:
            return u"%(this)s in %(parent)s" % \
                {
                    'this': self.display_name_and_type(),
                    'parent': self.parent.display_name_and_type()
                }

    def __unicode__(self):
        ''' print Area name from its Kind and parent

Example: name=Bamako, kind=District => District of Bamako '''

        # don't add-in kind if kind name is already part of name.
        # if (not self.parent) or (not self.kind) or self.name.startswith(self.kind.name):
        #    return self.name
        # else:
        #    return _(u"%(type)s of %(area)s.") % {'type': self.kind.name, \
        #                                              'area': self.name,}

        return self.name

################################
# imported from health_facility


class FacilityType(models.Model):
    name = models.CharField(max_length=100)
    slug = models.CharField(max_length=30, unique=True)

    class Meta:
        verbose_name = _("Facility Type")
        verbose_name_plural = _("Facility Types")

    def __unicode__(self):
        return self.name


class Facility(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=64, blank=True, null=False)
    type = models.ForeignKey(FacilityType, blank=True, null=True)

    catchment_areas = models.ManyToManyField(
        Area, null=True, blank=True, related_name='catchment')
    location = models.ForeignKey(Point, null=True, blank=True)
    area = models.ForeignKey(
        Area, null=True, blank=True, related_name='facility',)

    parent = models.ForeignKey(
        'self', null=True, blank=True, related_name='facility')

    class Meta:
        verbose_name = _("Facility")
        verbose_name_plural = _("Facilities")

    def __unicode__(self):
        return u"%s %s" % (self.type, self.name)

    def is_root(self):
        if self.parent == None:
            return True
        else:
            return False

    def get_children(self):
        #import pdb; pdb.set_trace()

        children = self._default_manager.filter(parent=self)
        return children

    def get_descendants(self):
        descendants = children = self.get_children()

        for child in children:
            if child.has_children:
                descendants = descendants | child.descendants
        return descendants

    @property
    def is_child_node(self):
        children = self._default_manager.filter(parent=self).count()
        if children > 0:
            return False
        else:
            return True

    @property
    def has_children(self):
        children = self._default_manager.filter(parent=self).count()
        if children > 0:
            return True
        else:
            return False

    @property
    def children(self,):
        return self.get_children()

    @property
    def descendants(self,):
        return self.get_descendants()
