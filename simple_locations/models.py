#!/usr/bin/env python
# encoding=utf-8
# vim: ai ts=4 sts=4 et sw=4


from django.db import models
from django.utils.translation import ugettext as _, ugettext_lazy as __
# from code_generator.fields import CodeField # removed so that we can use
# South
from mptt.models import MPTTModel
from mptt.managers import TreeManager


class Point(models.Model):

    class Meta:
        verbose_name = __("Point")
        verbose_name_plural = __("Points")
        app_label = 'simple_locations'

    latitude = models.DecimalField(max_digits=13, decimal_places=10)
    longitude = models.DecimalField(max_digits=13, decimal_places=10)

    def __unicode__(self):
        return _(u"%(lat)s, %(lon)s") % {'lat': self.latitude,
                                         'lon': self.longitude}


class AreaType(models.Model):

    class Meta:
        verbose_name = __("Area Type")
        verbose_name_plural = __("Area Types")
        app_label = 'simple_locations'

    name = models.CharField(max_length=100)
    slug = models.CharField(max_length=30, unique=True)

    def __unicode__(self):
        return _(self.name)


class Area(MPTTModel):
    # added to squash mptt deprecatino of .tree warning
    objects = tree = TreeManager()

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
    kind = models.ForeignKey('AreaType', blank=True, null=True)
    location = models.ForeignKey(Point, blank=True, null=True)
    parent = models.ForeignKey('self', blank=True, null=True,
                               related_name='children')

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

    def __unicode__(self):
        ''' print Area name from its Kind and parent

        Example: Bamako '''

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
        verbose_name = __("Facility Type")
        verbose_name_plural = __("Facility Types")
        app_label = 'simple_locations'

    def __unicode__(self):
        return self.name


class Facility(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=64, blank=True, null=False)
    type = models.ForeignKey(FacilityType, blank=True, null=True)

    catchment_areas = models.ManyToManyField(Area, related_name='catchment')
    location = models.ForeignKey(Point, null=True, blank=True)
    area = models.ForeignKey(Area, null=True, blank=True, related_name='facility')

    parent = models.ForeignKey('self', null=True, blank=True, related_name='facility')

    class Meta:
        verbose_name = __("Facility")
        verbose_name_plural = __("Facilities")
        app_label = 'simple_locations'

    def __unicode__(self):
        return u"%s %s" % (self.type, self.name)

    def is_root(self):
        if self.parent is None:
            return True
        else:
            return False

    def get_children(self):
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
