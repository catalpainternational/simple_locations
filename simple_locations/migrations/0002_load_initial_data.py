# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations


def load_initial_data(apps, schema_editor):
    # this migration used to load the initial data, we do not want this anymore, but are leaving it here
    # to preserve migration history
    # call_command('loaddata', 'initial_data', app_label='simple_locations')
    pass


class Migration(migrations.Migration):

    dependencies = [("simple_locations", "0001_initial")]

    operations = [
        migrations.RunPython(load_initial_data),
    ]
