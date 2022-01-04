# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from typing import List, Tuple

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = []  # type: List[Tuple[str, str]]

    operations = [
        migrations.CreateModel(
            name="Area",
            fields=[
                ("id", models.AutoField(verbose_name="ID", serialize=False, auto_created=True, primary_key=True)),
                ("name", models.CharField(max_length=100)),
                ("code", models.CharField(max_length=50)),
                ("lft", models.PositiveIntegerField(editable=False, db_index=True)),
                ("rght", models.PositiveIntegerField(editable=False, db_index=True)),
                ("tree_id", models.PositiveIntegerField(editable=False, db_index=True)),
                ("level", models.PositiveIntegerField(editable=False, db_index=True)),
            ],
            options={
                "verbose_name": "Area",
                "verbose_name_plural": "Areas",
            },
        ),
        migrations.CreateModel(
            name="AreaType",
            fields=[
                ("id", models.AutoField(verbose_name="ID", serialize=False, auto_created=True, primary_key=True)),
                ("name", models.CharField(max_length=100)),
                ("slug", models.CharField(unique=True, max_length=30)),
            ],
            options={
                "verbose_name": "Area Type",
                "verbose_name_plural": "Area Types",
            },
        ),
        migrations.CreateModel(
            name="Facility",
            fields=[
                ("id", models.AutoField(verbose_name="ID", serialize=False, auto_created=True, primary_key=True)),
                ("name", models.CharField(max_length=100)),
                ("code", models.CharField(max_length=64, blank=True)),
                ("area", models.ForeignKey(related_name="facility", blank=True, to="simple_locations.Area", null=True, on_delete=models.CASCADE)),
                ("catchment_areas", models.ManyToManyField(related_name="catchment", to="simple_locations.Area")),
            ],
            options={
                "verbose_name": "Facility",
                "verbose_name_plural": "Facilities",
            },
        ),
        migrations.CreateModel(
            name="FacilityType",
            fields=[
                ("id", models.AutoField(verbose_name="ID", serialize=False, auto_created=True, primary_key=True)),
                ("name", models.CharField(max_length=100)),
                ("slug", models.CharField(unique=True, max_length=30)),
            ],
            options={
                "verbose_name": "Facility Type",
                "verbose_name_plural": "Facility Types",
            },
        ),
        migrations.CreateModel(
            name="Point",
            fields=[
                ("id", models.AutoField(verbose_name="ID", serialize=False, auto_created=True, primary_key=True)),
                ("latitude", models.DecimalField(max_digits=13, decimal_places=10)),
                ("longitude", models.DecimalField(max_digits=13, decimal_places=10)),
            ],
            options={
                "verbose_name": "Point",
                "verbose_name_plural": "Points",
            },
        ),
        migrations.AddField(
            model_name="facility",
            name="location",
            field=models.ForeignKey(blank=True, to="simple_locations.Point", null=True, on_delete=models.CASCADE),
        ),
        migrations.AddField(
            model_name="facility",
            name="parent",
            field=models.ForeignKey(related_name="facility", blank=True, to="simple_locations.Facility", null=True, on_delete=models.CASCADE),
        ),
        migrations.AddField(
            model_name="facility",
            name="type",
            field=models.ForeignKey(blank=True, to="simple_locations.FacilityType", null=True, on_delete=models.CASCADE),
        ),
        migrations.AddField(
            model_name="area",
            name="kind",
            field=models.ForeignKey(blank=True, to="simple_locations.AreaType", null=True, on_delete=models.CASCADE),
        ),
        migrations.AddField(
            model_name="area",
            name="location",
            field=models.ForeignKey(blank=True, to="simple_locations.Point", null=True, on_delete=models.CASCADE),
        ),
        migrations.AddField(
            model_name="area",
            name="parent",
            field=models.ForeignKey(related_name="children", blank=True, to="simple_locations.Area", null=True, on_delete=models.CASCADE),
        ),
        migrations.AlterUniqueTogether(
            name="area",
            unique_together=set([("code", "kind")]),
        ),
    ]
