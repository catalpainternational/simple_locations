# simple_locations

The common location package used for catalpa's projects. A hierarchical tree of geographical locations supporting location type and GIS data.

## Admin

The admin site is set up to use Modeltranslations (if available in the parent app)

For modeltranslations, please remember to run `sync_translation_fields` in order to get `name_en`, `name_tet` etc. fields.

## Environment

This is intended to be compatible with:

- Django 5.2 LTS (dev/tests); library code targets Django 3.2+
- Python 3.10+ (3.12 recommended for local dev/tests)

```sh
gh repo clone catalpainternational/simple_locations
cd simple_locations
python -m venv env
. env/bin/activate
pip install pip-tools
pip-sync requirements.txt dev.txt
pre-commit install
```

### Tests

Install dev dependencies with Poetry, then run all tests (PostGIS + GDAL/GEOS required; see `tests/test_settings.py`):

```sh
poetry run pytest
```

**Postgres.app (macOS):** with PostGIS enabled, tests use your OS user on `localhost:5432` (no password). pytest-django creates and destroys a `simple_locations_test` database if your role has `CREATEDB`.

**Docker PostGIS** (official image defaults):

```sh
docker run --rm -p 5432:5432 -e POSTGRES_PASSWORD=postgres postgis/postgis:16-3.4
POSTGRES_USER=postgres POSTGRES_PASSWORD=postgres POSTGRES_DB=postgres poetry run pytest
```

Override connection with `POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_DB`, `POSTGRES_HOST`, or `POSTGRES_PORT`. Use `pytest --reuse-db` to keep the test database between runs.

On macOS, set `GDAL_LIBRARY_PATH` and `GEOS_LIBRARY_PATH` in the shell (forwarded in `tests/test_settings.py`).

### Pre Commit

If `pre-commit` is installed your code will be checked before commit.
This includes

- black
- flake8
- isort
- mypy

The same checks are run on push. See `pytest.yaml` for details on the checks being run.

### New Release

For a new release, change the `version` property in pyproject.toml and push a git tag with the version number
For instance at time of writing the version is `3.1.4` with the tag `v3.1.4`

See `build.yaml` for details on release tagging
## Changelog

- Version 3.1.4
  - Migrating JSON views from openly

- Version 3.1.3
  - Added `intersects_area` function

- Version 3.1.2
  - Development tests use psycopg3 (`psycopg[binary]`); runtime code uses Django's `DateRange` (no psycopg2 import)

- Version 3.1.1
  - Added "border" fields
  - Added a model for "projected" areas in EPSG:3857
  - Added commands for border generation and
  - `./manage.py` and associated project code

- Version 3.0.1

  - Poetry for dependency + packaging
  - Releases are automated by pushing a `vx.x.x` tag to github

- Version 3.0 (not on pypi)

  - Code style changes (black, flake8)

- Version 2.77

  - first pass of updates for Python 3.8+ and Django 3.1+

- Version 2.75

  - add modeltranslations

- Version 2.74

  - fix CORS issue breaking maps in AreaAdmin
  - typo in AreaChildrenInline

- Version 2.73

  - add an inline showing children to the Area admin
  - make the `geom` field optional

- Version 2.72
  - optionally use django_extensions' ForeignKeyAutocompleteAdmin in admin interface


## Manually Uploading a new version to PyPi

Bump `pyproject.toml`
Then run `poetry build` and `poetry publish`

```bash
poetry build
poetry publish
```

See the file `build.yml` for the workflow
