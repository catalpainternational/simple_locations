import os
import shutil
import tempfile
import urllib
import zipfile
from pathlib import Path

from django.contrib.gis.gdal import DataSource
from django.contrib.gis.geos import GEOSGeometry, MultiPolygon
from django.core.management.base import BaseCommand

from django.db import IntegrityError

from typing import Any

from simple_locations.models import Area, AreaType

area_definition_set = {
    "png_llg_boundaries_2011census_region.shp": {
        "areatype": "llg",
        "name": "LLGNAME",
        "code": "GEOCODE",
    },
    "png_dist_boundaries_2011census_region.shp": {
        "areatype": "district",
        "name": "DISTNAME",
        "code": "GEOCODE",
    },
    "png_prov_boundaries_2011census_region.shp": {
        "areatype": "province",
        "name": "PROVNAME",
        "code": "PROVID",
    },
}


class Command(BaseCommand):

    help = """Import data from NSO PNG Boundaries zip file"""

    def handle(self, *args: Any, **options: Any):
        self.import_zip()
        # self.import_directory('/home/josh/Downloads/NSO_PNG Boundaries')

    def import_zip(
        self,
        zip_url: str = "https://png-data.sprep.org/system/files/NSO_PNG%20Boundaries.zip",
    ):

        with urllib.request.urlopen(
            zip_url
        ) as response, tempfile.NamedTemporaryFile() as tmp_file:
            shutil.copyfileobj(response, tmp_file)
            with zipfile.ZipFile(tmp_file) as tmpzip:
                with tempfile.TemporaryDirectory() as tmpdirname:
                    tmpzip.extractall(tmpdirname)
                    self.import_directory(tmpdirname)
    
    def import_directory(self, tmpdirname: str):
      for filename in [
            f for f in os.listdir(tmpdirname) if f.endswith(".shp")
        ]:
                        
        area_definition = area_definition_set[filename]
        area_type = AreaType.objects.get_or_create(
            name=area_definition["areatype"],
            slug=area_definition["areatype"],
        )[0]  # type: AreaType
        self.import_shp(
            shape_path=Path(tmpdirname) / filename,
            area_type=area_type,
            field_mapping=area_definition,
        )

    def import_shp(self, shape_path: Path, area_type: AreaType, field_mapping: dict) -> None:

        for feature in DataSource(str(shape_path))[0]:
            self.import_feature(
                feature=feature, area_type=area_type, field_mapping=field_mapping
            )

    def import_feature(
        self,
        feature,
        area_type: AreaType,
        field_mapping: dict,
        database_srid: int = 4326,
    ):
        # Transform the geometry to a MultiPolygon if it is a Single Polygon
        # This is because a Shapefile may contain a data type which we don't cover (like a Polygon)
        geom = feature.geom.geos if isinstance(feature.geom.geos, MultiPolygon) else MultiPolygon(feature.geom.geos)
        code = str(feature.get(field_mapping["code"]))
        geometry_srid = feature.geom.srid

        # Transform the geometry if required
        # to suit the database SRID
        asset_geometry = GEOSGeometry(geom, srid=geometry_srid)
        if geometry_srid != database_srid:
            asset_geometry.transform(database_srid)

        try:
            area = Area.objects.create(
                name=feature.get(field_mapping["name"]),
                code=code,
                kind=area_type,
                geom=asset_geometry,
            )
            return area
        except IntegrityError as E:
            self.stderr.write(self.style.ERROR(f'Error writing code {code}: {E}'[:140]+'...' ))
