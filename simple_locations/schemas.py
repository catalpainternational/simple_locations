from typing import Any, Dict, List, Literal, Tuple, Union

from pydantic import BaseModel, Field

Coords = Tuple[float, float]
CoordsA = List[Coords]


class Point(BaseModel):
    type: Literal["Point"]
    coordinates: Coords


class MultiPoint(BaseModel):
    type: Literal["MultiPoint"]
    coordinates: CoordsA


class Polygon(BaseModel):
    type: Literal["Polygon"]
    coordinates: Union[List[Coords], List[CoordsA]]


class MultiPolygon(BaseModel):
    type: Literal["MultiPolygon"]
    coordinates: Union[
        List[List[Coords]],
        List[List[List[Coords]]],
        List[List[List[List[Coords]]]],
    ]


class Feature(BaseModel):
    type: Literal["Feature"] = "Feature"
    geometry: Union[Point, MultiPoint, Polygon, MultiPolygon] = Field(..., discriminator="type")
    id: Union[int, str]
    properties: Dict[str, Any]


class FeatureCollection(BaseModel):
    type: Literal["FeatureCollection"] = "FeatureCollection"
    features: List[Feature]
