from django.core.management.base import BaseCommand
from django.db import connection


class Scripts:

    populate_simple_locations_projectedarea = """
        TRUNCATE simple_locations_projectedarea;
        INSERT INTO simple_locations_projectedarea (geom, area_id)
        SELECT ST_TRANSFORM(geom, 3857), id FROM simple_locations_area;
    """


class Command(BaseCommand):
    help = "My shiny new management command."

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        with connection.cursor() as c:
            self.stdout.write(self.style.SUCCESS(Scripts.populate_simple_locations_projectedarea))
            c.execute(Scripts.populate_simple_locations_projectedarea)
