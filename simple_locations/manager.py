import io

from django.contrib.gis.db.models.functions import AsGeoJSON
from django.db import models
from django.http import HttpResponse

from simple_locations.gis_functions import Multi, Quantize, Simplify


class AreaQueryset(models.QuerySet):
    def _annotate_geometries(self, simplify: float = 1e-3, quantize: int = 5) -> models.QuerySet:
        return self.annotate(
            geojson=AsGeoJSON(
                Multi(
                    Quantize(
                        Simplify(
                            "geom",
                            simplify=simplify,
                        ),
                        quantize=quantize,
                    )
                )
            )
        )

    def to_geojson(self, simplify: float = 1e-3, quantize: int = 5) -> str:
        """
        Intended to be a highly performant geoJSON generator, this is inspired by Django's
        geojson serializer but simplified, and carries out more operations in the DB including
        geometry simplifying and quantization

        This returns a string, in order to prevent multiple ser / de-ser calls
        """

        output = io.StringIO()  # Avoids a round-trip deserializer by using a raw StringIO
        prefix = """{"type": "FeatureCollection", "crs": {"type": "name", "properties": {"name": "EPSG:4326"}}, "features": ["""  # noqa: E501
        pattern = '{"type": "Feature", "geometry": %s, "properties": {"id": %s } }'
        suffix = "]}"

        output.write(prefix)
        is_first = True
        for obj in self.filter(geom__isnull=False)._annotate_geometries(simplify=simplify, quantize=quantize):
            if is_first:
                is_first = False
            else:
                output.write(",")
            output.write(pattern % (obj.geojson, obj.id))

        output.write(suffix)

        return output.getvalue()

    def to_response(self):
        """
        Directly return a valid HTTPResponse
        """
        return HttpResponse(content_type="application/json", content=self.to_geojson())
