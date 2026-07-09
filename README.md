# simple_locations

The common location package used for catalpa's projects. A hierarchical tree of geographical locations supporting location type and GIS data.

## Admin

The admin site is set up to use Modeltranslations (if available in the parent app)

For modeltranslations, please remember to run `sync_translation_fields` in order to get `name_en`, `name_tet` etc. fields.

## Compatibility

`simple-locations` ships **two parallel lines** — pick by the stack you run. Full
matrix and per-version notes are in [CHANGELOG.md](CHANGELOG.md).

| Your stack | Pin |
|------------|-----|
| django-ninja 1.x · pydantic 2 · Django 5.x · psycopg3 · Python 3.10+ | `simple-locations>=4.2.0` |
| django-ninja 0.x · pydantic 1 · Django ≤ 4.2 · psycopg2 · Python 3.9+ | `simple-locations>=4.0.3,<4.1` |

> ⚠️ A bare `simple-locations>=4.0.3` resolves to **4.2.0** on a fresh install
> unless another constraint (e.g. `django-ninja<1`) holds it down. On the
> pydantic-1 line, cap it: `>=4.0.3,<4.1`.

## Development environment

Dev and tests target **Django 5.2** on **Python 3.10+** (3.12 recommended).

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

Releases publish to PyPI automatically via the **Publish to PyPI** workflow
(`.github/workflows/publish.yml`) when a GitHub Release is created:

1. Bump `version` in `pyproject.toml` and commit (choose the line — 4.0.x is
   pydantic-1, 4.2.x is pydantic-2; see [CHANGELOG.md](CHANGELOG.md)).
2. Create a GitHub Release with a matching tag (e.g. `v4.2.0`).
3. The workflow builds (`poetry build`) and uploads with
   `pypa/gh-action-pypi-publish` using the `PYPI_API_TOKEN` secret.

The workflow is idempotent (`skip-existing`), so re-running for an already-published
version is a no-op.

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for the full version history and the
compatibility matrix.
