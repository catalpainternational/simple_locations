from django.core.management.base import BaseCommand

from simple_locations.models import Area


class Command(BaseCommand):

    help = """prints all districts in a form that's easy to import into excel"""

    def handle(self, **options):
        print("id\tname\ttype\tparent_id\tparent_name\tparent_type")
        for a in Area.tree.all():
            print(
                "%d\t%s\t%s\t%d\t%s\t%s"
                % (
                    a.pk,
                    a.name,
                    a.kind.name,
                    a.parent.pk if a.parent else -1,
                    a.parent.name if a.parent else "",
                    a.parent.kind.name if a.parent else "",
                )
            )
