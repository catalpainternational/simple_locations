# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations
from django.core.management import call_command


def load_initial_data(apps, schema_editor):
    call_command('loaddata', 'initial_data', app_label='simple_locations')


class Migration(migrations.Migration):

    dependencies = [
        ('simple_locations', '0001_initial')
    ]

    operations = [
        migrations.RunPython(load_initial_data),
    ]
