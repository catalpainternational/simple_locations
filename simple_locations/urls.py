from django.conf.urls import url
from simple_locations.views import edit_location, add_location, delete_location, render_location, simple_locations, area_search

urlpatterns = [
    url(r'^simple_locations/edit/(?P<area_id>[0-9]+)/$', edit_location),
    url(r'^simple_locations/add/((?P<parent_id>[0-9]+)/){0,1}$', add_location),
    url(r'^simple_locations/delete/(?P<area_id>[0-9]+)/$', delete_location),
    url(r'^simple_locations/render_tree/$', render_location),
    url(r'^simple_locations/$', simple_locations),
    url(r'^areasearch/$', area_search),
]
