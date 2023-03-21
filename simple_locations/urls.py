from django.urls import path

from simple_locations.api import api
from simple_locations.models import Area
from simple_locations.views import (
    AreaJSONLayerView,
    ChildAreasJSONLayerView,
    add_location,
    area_search,
    delete_location,
    edit_location,
    render_location,
    simple_locations,
)

app_name = "simple_locations"

urlpatterns = [
    path("simple_locations/edit/<int:area_id>/", edit_location),
    path("simple_locations/add/", add_location),
    path("simple_locations/add/<int:parent_id>/", add_location),
    path("simple_locations/delete/<int:area_id>/", delete_location),
    path("simple_locations/render_tree/", render_location),
    path("simple_locations/", simple_locations),
    path("areasearch/", area_search),
    path(
        "data.geojson/",
        AreaJSONLayerView.as_view(model=Area, properties=("name", "area_activities__activity__name")),
        name="data",
    ),
    path(
        "<int:area>/children.geojson/",
        ChildAreasJSONLayerView.as_view(model=Area, properties=("name", "id", "code", "parent_id")),
        name="children",
    ),
    path("api/", api.urls),
]
