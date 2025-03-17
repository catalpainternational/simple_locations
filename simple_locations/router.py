from typing import Generator, List, Tuple

from ninja import Router

from geojson_pydantic import FeatureCollection, Feature

from simple_locations import model_schemas, models

router = Router(tags=["SimpleLocations"])

SIMPLIFICATION_LEVELS: Tuple[float, ...] = (0.0, 0.0001, 0.001, 0.01, 0.1, 0.5)


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


@router.get("/area/by-id/{area_id}.geojson", response=Feature)
def area_id(request, area_id: int):
    """
    Returns the geometry of a single Area
    as a single GeoJSON Feature
    """
    features: Generator[Feature, None, None] = models.Area.features.filter(pk=area_id).to_features()
    return Feature.parse_obj(next(features))


@router.get("/area/by-parent/{area_id}-s{simplify}-q{quantize}.geojson", response=FeatureCollection)
def area_children_compressed(request, area_id: int, simplify: int, quantize: int):
    """
    Returns the direct descendants of a given Area as a FeatureCollection
    applying compression methods
    """
    return models.Area.features.filter(parent=area_id).to_featurecollection(
        simplify=SIMPLIFICATION_LEVELS[simplify], quantize=quantize
    )


@router.get("/area/by-parent/{area_id}.geojson", response=FeatureCollection)
def area_children(request, area_id: int):
    """
    Returns the direct descendants of a given Area as a FeatureCollection
    applying compression methods
    """
    return models.Area.features.filter(parent=area_id).to_featurecollection()


@router.get("/area/by-type/{area_type}-s{simplify}-q{quantize}.geojson", response=FeatureCollection)
def area_type_compressed(request, area_type: str, simplify: int, quantize: int):
    """
    Returns all areas of a given type
    appliying simplification and quantization
    """
    return models.Area.features.filter(kind__slug=area_type).to_featurecollection(
        simplify=SIMPLIFICATION_LEVELS[simplify], quantize=quantize
    )


@router.get("/area/by-type/{area_type}.geojson", response=FeatureCollection)
def area_type(request, area_type: str):
    """
    Returns all areas of a given type
    """
    return models.Area.features.filter(kind__slug=area_type).to_featurecollection()
