import os
import shutil
import tempfile
import urllib
import zipfile
from pathlib import Path
from typing import Any, List, NamedTuple
from warnings import warn

from django.contrib.gis.db.models import Union
from django.contrib.gis.gdal.datasource import DataSource
from django.contrib.gis.geos import GEOSGeometry, MultiPolygon
from django.core.management.base import BaseCommand
from django.db import IntegrityError

from simple_locations.models import Area, AreaType


class RenameDistrict(NamedTuple):
    nso_name: str
    wiki_name: str


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
        self.merge_districts()
        self.rebuild_tree()
        self.perform_rename()

    def import_zip(
        self,
        zip_url: str = "https://png-data.sprep.org/system/files/NSO_PNG%20Boundaries.zip",
    ):

        with urllib.request.urlopen(zip_url) as response, tempfile.NamedTemporaryFile() as tmp_file:  # type: ignore
            shutil.copyfileobj(response, tmp_file)
            with zipfile.ZipFile(tmp_file) as tmpzip:
                with tempfile.TemporaryDirectory() as tmpdirname:
                    tmpzip.extractall(tmpdirname)
                    self.import_directory(tmpdirname)

    def import_directory(self, tmpdirname: str):
        self.stderr.write(self.style.NOTICE("Importing shapes"))
        for filename in [f for f in os.listdir(tmpdirname) if f.endswith(".shp")]:

            area_definition = area_definition_set[filename]
            area_type = AreaType.objects.get_or_create(
                name=area_definition["areatype"],
                slug=area_definition["areatype"],
            )[
                0
            ]  # type: AreaType
            self.stderr.write(self.style.NOTICE(f"Importing {tmpdirname} / {filename}"))
            self.import_shp(
                shape_path=Path(tmpdirname) / filename,
                area_type=area_type,
                field_mapping=area_definition,
            )

    def import_shp(self, shape_path: Path, area_type: AreaType, field_mapping: dict) -> None:

        for feature in DataSource(str(shape_path))[0]:
            self.import_feature(feature=feature, area_type=area_type, field_mapping=field_mapping)

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

        if Area.objects.filter(code=code).exists():
            self.stderr.write(self.style.NOTICE(f"Skip {code} because it already exists"))
            return Area.objects.get(code=code)
        try:
            area = Area.objects.create(
                name=feature.get(field_mapping["name"]),
                code=code,
                kind=area_type,
                geom=asset_geometry,
            )
            return area
        except IntegrityError as E:
            self.stderr.write(self.style.ERROR(f"Error writing code {code}: {E}"[:140] + "..."))

    def merge_districts(self):
        """
        As we do not have a unified "Country" shape, merge the Districts to create the top level
        """
        self.stderr.write(self.style.SUCCESS("Merge provinces"))
        country_level_area = Area.objects.get_or_create(
            kind=AreaType.objects.get_or_create(name="country", slug="country")[0],
            geom=Area.objects.filter(kind__name="province").aggregate(Union("geom"))[
                "geom__union"
            ],  # Multipolygon object
            name="Papua New Guinea",
            code="PNG",
        )[0]

        for d in Area.objects.filter(kind__name="province"):
            d.parent = country_level_area
            d.save()

    def rebuild_tree(self):

        self.stderr.write(self.style.SUCCESS("Reset Area parent code"))
        for a in Area.objects.exclude(kind__name__in=["country", "province"]):
            try:
                a.parent = Area.objects.get(code=a.code[:-2])
                a.save()
            except Exception as E:
                warn(f"{E}")
                pass

        self.stderr.write(self.style.SUCCESS("Rebuild the locations Area tree"))
        Area.objects.rebuild()

    def perform_rename(self):

        sources = """Abau District	Abau District
        Aitape-Lumi District	Aitape/Lumi District
        Alotau District	Alotau District
        Ambunti-Dreikikier District	Ambunti/Drekikier District
        Anglimp-South Waghi District	Anglimp/South Waghi District
        Angoram District	Angoram District
        Bogia District	Bogia District
        Bulolo_District	Bulolo District
        Central Bougainville District	Central Bougainville District
        Chuave District	Chuave District
        Daulo District	Daulo District
        Dei District	Dei District
        Esa'ala District	Esa'ala District
        Finschhafen District	Finschafen District
        Gazelle District	Gazelle District
        Goilala District	Goilala District
        Goroka District	Goroka District
        Gumine District	Gumine District
        Henganofi District	Henganofi District
        Huon District	Huon District
        Ialibu-Pangia District	Ialibu/Pangia District
        Ijivitari District	Ijivitari District
        Imbonggu District	Imbonggu District
        Jimi District	Jimi District
        Kabwum District	Kabwum District
        Kagua-Erave District	Kagua/Erave District
        Kainantu District	Kainanatu District
        Kairuku-Hiri District	Kairuku - Hiri District
        Kandep District	Kandep District
        Kandrian-Gloucester District	Kandrian/Gloucester District
        Karimui-Nomane District	Karimui/Nomane District
        Kavieng District	Kavieng District
        Kerema District	Kerema District
        Kerowagi District	Kerowagi District
        Kikori District	Kikori District
        Kiriwini-Goodenough District	Kiriwina-Goodenough District
        Kokopo District	Kokopo District
        Komo-Magarima District	Komo/Magarima District
        Kompiam Ambum District	Kompiam District
        Koroba-Kopiago District	Koroba/Kopiago District
        Kundiawa-Gembogl District	Kundiawa/Gembogl District
        Lae District	Lae District
        Lagaip-Porgera District	Lagaip/Pogera District
        Lufa District	Lufa District
        Madang District	Madang District
        Manus District	Manus District
        Maprik District	Maprik District
        Markham District	Markham District
        Mendi-Munihu District	Mendi/Munihu District
        Menyamya District	Menyamya District
        Middle Fly District	Middle Fly District
        Middle Ramu District	Middle Ramu District
        Mount Hagen District	Mt Hagen District
        Mul-Baiyer District	Mul/Baiyer District
        Namatanai District	Namatanai District
        National Capital District	National Capital District
        Nawae District	Nawae District
        Nipa-Kutubu District	Nipa/Kutubu District
        North Bougainville District	North Bougainville District
        North Fly District	North Fly District
        North Waghi District	North Waghi District
        Nuku District	Nuku District
        Obura-Wonenara District	Obura/Wonenara District
        Okapa District	Okapa District
        Pomio District	Pomio District
        Rabaul District	Rabaul District
        Rai Coast District	Rai Coast District
        Rigo District	Rigo District
        Samarai-Murua District	Samarai-Murua District
        Sina Sina-Yonggomugl District	Sina Sina Yonggomugl District
        Sohe District	Sohe District
        South Bougainville District	South Bougainville District
        South Fly District	South Fly District
        Sumkar District	Sumkar District
        Talasea District	Talasea District
        Tambul-Nebilyer District	Tambul/Nebilyer District
        Tari-Pori District	Tari/Pori District
        Tawae-Siassi District	Tawae/Siassi District
        Telefomin District	Telefomin District
        Unggai-Benna District	Unggai/Benna District
        Usino Bundi District	Usino Bundi District
        Vanimo-Green River District	Vanimo/Green River District
        Wabag District	Wabag District
        Wapenamanda District	Wapenamanda District
        Wewak District	Wewak District
        Wosera-Gawi District	Wosera Gawi District
        Yangoru-Saussia District	Yangoru Saussia District"""

        renames = []  # type: List[RenameDistrict]

        for s in sources.split("\n"):
            n = s.split("\t")
            renames.append(RenameDistrict(n[1].strip(), n[0].strip()))

        # Area.objects.all().delete()
        self.stdout.write(self.style.MIGRATE_HEADING("~~~ Starting rename ~~~"))
        for rename in renames:
            try:
                area = Area.objects.get(name=rename.nso_name, kind__name="district")
            except Area.DoesNotExist:
                self.stdout.write(self.style.WARNING(f'Area does not exist: "{rename.nso_name}"'))
                continue

            if area.name == rename.wiki_name:
                self.stdout.write(self.style.SUCCESS(f'No change: "{rename.nso_name}"'))
            else:
                area.name = rename.wiki_name
                area.save()
                self.stdout.write(
                    self.style.SUCCESS(f'Successfully renamed: "{rename.nso_name}" to "{rename.wiki_name}s')
                )
