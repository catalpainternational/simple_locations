from ninja import ModelSchema

from simple_locations.models import Area, AreaType


class AreaModelSchema(ModelSchema):
    class Meta:
        model = Area
        fields = ["name", "id", "kind", "parent"]


class AreaTypeModelSchema(ModelSchema):
    class Meta:
        model = AreaType
        fields = ["id", "name", "slug"]
