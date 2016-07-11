# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations
from django.core.management import call_command


fixture = 'initial_data'

def load_fixture(apps, schema_editor):
    call_command('loaddata', fixture, app_label='simple_locations')


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.RunPython(load_fixture),
    ]
