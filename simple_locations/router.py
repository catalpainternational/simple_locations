from typing import List

from ninja import Router

from simple_locations import model_schemas, models, schemas

router = Router(tags=["SimpleLocations"])


@router.get("/area/list.json", response=List[model_schemas.AreaModelSchema])
def area_list(request):
    """
    Returns a list of area information: name, id, parent id
    """
    return models.Area.objects.all()


@router.get("/areatype/list.json", response=List[model_schemas.AreaTypeModelSchema])
def area_type_list(request):
    """
    List the different area types
    """
    return models.AreaType.objects.all()


@router.get("/area/by-id/{area_id}.geojson", response=schemas.Feature)
def area_id(request, area_id: int):
    """
    Returns the geometry of a single Area
    as a single GeoJSON Feature
    """
    features = models.Area.features.filter(pk=area_id).to_features()
    return schemas.Feature.parse_obj(next(features))


@router.get("/area/by-parent/{area_id}.geojson", response=schemas.FeatureCollection)
def area_children(request, area_id: int):
    """
    Returns the direct descendants of a given Area as a FeatureCollection
    """
    return models.Area.features.filter(parent=area_id).to_featurecollection()


@router.get("/area/by-type/{area_type}.geojson", response=schemas.FeatureCollection)
def area_type(request, area_type: str):
    """
    Returns all areas of a given type
    """
    return models.Area.features.filter(kind__slug=area_type).to_featurecollection()
