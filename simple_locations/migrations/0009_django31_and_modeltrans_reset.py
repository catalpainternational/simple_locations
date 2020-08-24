# Generated by Django 3.1 on 2020-08-24 04:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("simple_locations", "0008_auto_20200804_0554"),
    ]

    _operations = [
        migrations.AddField(
            model_name="area",
            name="name_en",
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name="areatype",
            name="name_en",
            field=models.CharField(max_length=100, null=True),
        ),
    ]

    operations = [
        migrations.AlterField(
            model_name="area",
            name="level",
            field=models.PositiveIntegerField(editable=False),
        ),
        migrations.AlterField(
            model_name="area",
            name="lft",
            field=models.PositiveIntegerField(editable=False),
        ),
        migrations.AlterField(
            model_name="area",
            name="rght",
            field=models.PositiveIntegerField(editable=False),
        ),
        migrations.SeparateDatabaseAndState(
            database_operations=(), state_operations=_operations
        ),
    ]
