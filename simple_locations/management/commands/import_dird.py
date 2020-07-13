from django.core.management.base import BaseCommand
from simple_locations.models import Area, AreaType
import zipfile
import shapefile
import tempfile
import urllib
import shutil
from pathlib import Path
import os
from django.contrib.gis.gdal import DataSource

class Command(BaseCommand):

    help = """Import data from NSO PNG Boundaries zip file"""

    def handle(self, **options):
        
        url = 'https://png-data.sprep.org/system/files/NSO_PNG%20Boundaries.zip'
        database_srid = 4326  # Corresponding to 'Area' srid

        with urllib.request.urlopen(url) as response:
            with tempfile.NamedTemporaryFile() as tmp_file:
                shutil.copyfileobj(response, tmp_file)

                with zipfile.ZipFile(tmp_file) as tmpzip:
                    with tempfile.TemporaryDirectory() as tmpdirname:
                        tmpzip.extractall(tmpdirname)

                        # Mapping the file names to area types
                        # Maybe get a KeyError
                        area_definition = {
                            "png_llg_boundaries_2011census_region.shp": [{"areatype": "llg", "name": "LLGNAME", "code": "GEOCODE"}],
                            "png_dist_boundaries_2011census_region.shp": [{"areatype": "district", "name": "DISTNAME", "code": "GEOCODE"}],
                            "png_prov_boundaries_2011census_region.shp": [{"areatype": "province", "name": "PROVNAME", "code": "PROVID"}]
                        }

                        for filename in os.listdir(tmpdirname):
                            if not filename.endswith('.shp'):
                                continue

                            areatype = area_definition[filename]
                            shp_path = str(Path(tmpdirname) / filename)

                            for feature in Datasource(shp_path)[0]:
                                geom = MultiPolygon(feature.geom.geos)

                                asset_geometry = GEOSGeometry(geom, srid=feature.geom.srid)
                                if feature.geom.srid != database_srid:
                                    asset_geometry.transform(database_srid)

                                areatype = AreaType.objects.get_or_create(name=area_definition['areatype'], slug=area_definition['areatype'])[0]
                                Area.objects.create (
                                    name = feature.get(areatype['name']),
                                    code = feature.get(areatype['code']),
                                    kind = areatype,
                                    geom = asset_geometry
                                )
