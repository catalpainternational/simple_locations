from django.urls import path

from simple_locations.views import (
    add_location,
    area_search,
    delete_location,
    edit_location,
    render_location,
    simple_locations,
)

urlpatterns = [
    path("simple_locations/edit/<int:area_id>/", edit_location),
    path("simple_locations/add/", add_location),
    path("simple_locations/add/<int:parent_id>/", add_location),
    path("simple_locations/delete/<int:area_id>/", delete_location),
    path("simple_locations/render_tree/", render_location),
    path("simple_locations/", simple_locations),
    path("areasearch/", area_search),
]
