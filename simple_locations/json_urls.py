from django.conf.urls import url
# Return geoJSON representations of data

from . import json_views


urlpatterns = [
    url(r'^area/(?P<area_id>[0-9]+)/$', json_views.area, name='area'),
    url(r'^area/(?P<area_id>[0-9]+)/children/$', json_views.children, name='children'),
]