from ninja import ModelSchema

from simple_locations.models import Area, AreaType


class AreaModelSchema(ModelSchema):
    class Config:
        model = Area
        model_fields = ["name", "id", "kind", "parent"]


class AreaTypeModelSchema(ModelSchema):
    class Config:
        model = AreaType
        model_fields = ["id", "name", "slug"]
