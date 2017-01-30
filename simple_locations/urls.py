from django.conf.urls import url
from simple_locations.views import edit_location, add_location, delete_location, render_location, simple_locations, area_search

urlpatterns = (
    url(r'^simple_locations/edit/(?P<area_id>[0-9]+)/$', edit_location, name='edit-location'),
    url(r'^simple_locations/add/((?P<parent_id>[0-9]+)/){0,1}$', add_location, name='add-location'),
    url(r'^simple_locations/delete/(?P<area_id>[0-9]+)/$', delete_location, name='delete-location'),
    url(r'^simple_locations/render_tree/$', render_location, name='render-location'),
    url(r'^simple_locations/$', simple_locations, name='locations'),
    url(r'^areasearch/$', area_search, name='area-search'),
)
