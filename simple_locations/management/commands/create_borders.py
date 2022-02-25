from django.core.management.base import BaseCommand
from django.db import connection


class Scripts:

    init_topology = """
        -- Note:

        -- You may need to run the following SQL:

        -- CREATE EXTENSION postgis_topology;
        -- GRANT ALL ON SCHEMA topology TO dird;
        -- GRANT ALL ON ALL FUNCTIONS IN SCHEMA topology TO dird;
        -- GRANT ALL ON ALL TABLES IN SCHEMA topology TO dird;
        -- GRANT ALL ON ALL SEQUENCES IN SCHEMA topology TO dird;

        -- before running this script

        SELECT topology.CreateTopology('ma_topo', 3857, 15);
        CREATE TABLE if not exists simple_locations_topology(id serial, area_id int);
        SELECT topology.AddTopoGeometryColumn('ma_topo', 'public', 'simple_locations_topology', 'topo', 'POLYGON');
    """

    insert_areas = """
        -- This is fast
        insert into simple_locations_topology(area_id, topo)
            select id, topology.toTopoGeom(st_transform(geom, 3857), 'ma_topo', 1)
            from simple_locations_area where kind_id = 4;

    """

    insert_areas_2 = """
        -- This took about 3 - 4 minutes
        -- Topology inserts of polygons are known to be very slow
        insert into simple_locations_topology(area_id, topo)
            select id, topology.toTopoGeom(st_transform(geom, 3857), 'ma_topo', 1)
            from simple_locations_area where kind_id != 4;
    """

    populate_edge_table = """
        truncate simple_locations_border cascade;
        insert into simple_locations_border(id, geom, area_ids, area_types)
            select distinct e.edge_id, e.geom, ARRAY[]::int[], ARRAY[]::int[] from
            ma_topo.edge e;
    """

    populate_border_areas = """
        -- Populate the border -> area relations table
        truncate simple_locations_border_area CASCADE;

        -- "Outer" lines are where a line does not occur more than once
        -- for faces within a polygon

        -- The faces for a polygon are a relation between
        -- the toplogy layer to face:
        -- [simple_locations_topology] --> [topo.relation] --> [topo.face]

        with relation_faces as (
            -- Join faces table to relations table where the
            -- relation is valid. This should be all rows
            -- but just to be sure filter to type=3 and layer_id = 1
            select face_id, topogeo_id from ma_topo.face, ma_topo.relation r2
            where r2.element_type = 3  -- 1=point, 2=line, 3=polygon
            and r2.element_id = face.face_id
            and layer_id = 1
        )
        , area_faces as (
            -- Join from the topology to faces
            -- The resuult of this would be to match an 'area' to topo 'faces'
            -- Generally 'faces' here would be the smallest unit added (LLG level for PNG)
            select face_id, area_id from simple_locations_topology slt ,
            relation_faces rf
            where (slt.topo).id = rf.topogeo_id
        )

        , area_to_edge as (
            select ed.edge_id, area_faces.area_id from ma_topo.edge_data ed ,
            area_faces
            where ed.left_face = area_faces.face_id
            or ed.right_face = area_faces.face_id
        )
        -- Here a good troubleshooting return would be:
        -- select st_collect(geom) from area_to_edge natural left join ma_topo.edge_data where area_id = 822
        -- This will include all interior and exterior lines
        -- In order to correct this we need to drop any lines which are not part
        -- of only one face...
        --select * from area_to_edge natural left join ma_topo.edge_data where area_id = 822

        , count_edges as (
            select edge_id, count(edge_id), area_id from area_to_edge group by edge_id, area_id
        )

        --select st_collect(edge_data.geom) from count_edges, ma_topo.edge_data
        --	where count_edges.edge_id = edge_data.edge_id
        --	and count = 1
        --	and area_id = 822

        insert into simple_locations_border_area (border_id, area_id)
        select edge_id, area_id from count_edges where count = 1;
    """

    update_border_area_array = """
        with areas as (select border_id, array_agg(area_id) as area_ids from simple_locations_border_area group by border_id)
        update simple_locations_border b set area_ids =
            (select areas.area_ids from areas
            where areas.border_id = b.id)
            where b.id in (select border_id from areas)
    """

    update_border_type_array = """

        with area_types as (
            select border_id, array_agg(distinct slt.id) area_types from simple_locations_area sla,
                simple_locations_areatype slt,
                simple_locations_border_area slba
                where sla.kind_id = slt.id
                and slba.area_id = sla.id
                group by border_id
            ) update simple_locations_border b
            set area_types = (
                select area_types from area_types
                where area_types.border_id = b.id)
                where b.id in (select border_id from area_types)
    """

    remove_topology = """
        -- Undo all the changes, remove the topology layer
        select topology.DropTopoGeometryColumn('public', 'simple_locations_topology', 'topo');
        drop table simple_locations_topology;
        select topology.DropTopology('ma_topo')
    """


class Command(BaseCommand):
    help = "My shiny new management command."

    def add_arguments(self, parser):
        ...
        # parser.add_argument('sample', nargs='+')

    def handle(self, *args, **options):

        with connection.cursor() as c:
            self.stdout.write(self.style.SUCCESS(Scripts.init_topology))
            c.execute(Scripts.init_topology)
            self.stdout.write(self.style.SUCCESS(Scripts.insert_areas))
            c.execute(Scripts.insert_areas)
            self.stdout.write(self.style.SUCCESS(Scripts.insert_areas_2))
            c.execute(Scripts.insert_areas_2)
            self.stdout.write(self.style.SUCCESS(Scripts.populate_edge_table))
            c.execute(Scripts.populate_edge_table)
            self.stdout.write(self.style.SUCCESS(Scripts.populate_border_areas))
            c.execute(Scripts.populate_border_areas)

            self.stdout.write(self.style.SUCCESS(Scripts.update_border_type_array))
            c.execute(Scripts.update_border_type_array)

            self.stdout.write(self.style.SUCCESS(Scripts.update_border_area_array))
            c.execute(Scripts.update_border_area_array)

            self.stdout.write(self.style.SUCCESS(Scripts.remove_topology))
            c.execute(Scripts.remove_topology)

        # raise NotImplementedError()
