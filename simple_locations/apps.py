from django.apps import AppConfig


class SimpleLocationsConfig(AppConfig):
    """AppConfig for ``simple_locations``.

    Pins ``default_auto_field`` to ``AutoField`` so the app does not inherit a
    consuming project's ``DEFAULT_AUTO_FIELD``. Every model in this app was
    created with an integer ``AutoField`` primary key (see migrations
    ``0001``-onwards). Without this, a project that sets
    ``DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"`` (the default for
    ``startproject`` since Django 3.2) makes ``makemigrations`` perpetually want
    to emit an ``alter *_id`` migration for this installed package — noise the
    consumer cannot commit.

    This is intentionally ``AutoField`` (not ``BigAutoField``): it matches the
    existing migration history, so it is a metadata-only change with no schema
    migration for any existing consumer's data.
    """

    name = "simple_locations"
    default_auto_field = "django.db.models.AutoField"
