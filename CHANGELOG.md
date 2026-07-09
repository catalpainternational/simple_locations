# Changelog

All notable changes to `simple-locations` are documented here. The format is
based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and this
project aims to follow [Semantic Versioning](https://semver.org/).

## Compatibility matrix

`simple-locations` currently ships **two parallel lines**. Django itself is not
a declared dependency (your project provides it); the effective floor comes from
`django-ninja` and `psycopg`. Pick your line by the stack you run:

| Version | Python | django-ninja | pydantic | psycopg | Django (validated) | Use for |
|---------|--------|--------------|----------|---------|--------------------|---------|
| **4.2.0** (Latest) | ≥ 3.10 | `>=1.6,<2` | **2.x** | **psycopg3** | 5.2 (CI) | Modern stacks — Django 5.2, ninja 1.x, pydantic 2 |
| 4.1.0b2 | ≥ 3.9 | `<2` | 2.x | psycopg2 | — | Pre-release, **superseded by 4.2.0** — do not use |
| **4.0.3** | ≥ 3.9 | `>=0.21,<1` | **1.x** | **psycopg2** | 3.2–4.2 | Stacks pinned to `django-ninja<1` / pydantic 1 |
| 4.0.2 | ≥ 3.9 | `>=0.21,<0.22` | 1.x | psycopg2 | 3.2–4.2 | **Avoid** — over-tight ninja cap; use 4.0.3 |

**Which do I pin?**

- On **django-ninja 1.x / pydantic 2 / Django 5.x** → `simple-locations>=4.2.0`.
- On **django-ninja 0.x / pydantic 1 / Django ≤ 4.2** → `simple-locations>=4.0.3,<4.1`.

> ⚠️ A bare `simple-locations>=4.0.3` will resolve to **4.2.0** on a fresh
> install unless another constraint (e.g. `django-ninja<1`) holds it down. If you
> are on the pydantic-1 line, cap it: `>=4.0.3,<4.1`.

---

## [Unreleased]

## [4.2.0] - 2026-07-09

Django 5.2 support and a modernized stack (#50). This is the **pydantic-2 /
django-ninja-1** line.

### Changed
- **Django 5.2** validated in CI; **psycopg 3** replaces psycopg2; **django-ninja**
  moved to `>=1.6,<2` and **pydantic 2** (via `geojson-pydantic ^1.1`).
- Minimum **Python is now 3.10**.
- pydantic `parse_obj` → `model_validate`; `NinjaAPI(csrf=True)` → `NinjaAPI()`
  (ninja 1.x); `JSONObject` import moved to `django.db.models.functions.json`
  with a back-compat fallback; `DateRange` now imported from
  `django.contrib.postgres.fields.ranges` instead of `psycopg2.extras`.

### Notes
- Consumers pinned to `django-ninja<1` / pydantic 1 must stay on the **4.0.x**
  line (see the matrix above).

## [4.0.3] - 2026-07-09

Latest release on the **pydantic-1 / django-ninja-0** line.

### Fixed
- `AppConfig` now declares `default_auto_field = "django.db.models.AutoField"`,
  so the app stops inheriting a consuming project's `DEFAULT_AUTO_FIELD`. Without
  it, projects defaulting to `BigAutoField` saw `makemigrations` perpetually want
  an `alter *_id` migration for this installed package. Metadata-only — no schema
  migration for existing consumers.

### Changed
- Relaxed the `django-ninja` pin to `>=0.21,<1` (4.0.2 briefly capped it at
  `<0.22`, forcing a downgrade on consumers running 0.22.x).

## [4.0.2] - 2026-07-09

**Superseded by 4.0.3 — avoid.** First release carrying the `default_auto_field`
AppConfig fix, but it shipped a too-tight `django-ninja` cap (`<0.22`) that forced
a downgrade on consumers running 0.22.x.

## [4.0.0] - 2023-03-29

- New API; Django 3.2 required.

## Earlier (pre-4.0, from the previous in-README log)

- **3.1.4** — migrating JSON views from openly.
- **3.1.3** — added `intersects_area` function.
- **3.1.2** — dev tests use psycopg3 (`psycopg[binary]`); runtime uses Django's `DateRange` (no psycopg2 import).
- **3.1.1** — border fields; projected-areas model (EPSG:3857); border-generation commands; `./manage.py` and project code.
- **3.0.1** — Poetry for dependency + packaging; releases automated via `vx.x.x` tags.
- **3.0** (not on PyPI) — code-style changes (black, flake8).
- **2.77** — first pass of updates for Python 3.8+ and Django 3.1+.
- **2.75** — add modeltranslations.
- **2.74** — fix CORS issue breaking maps in AreaAdmin; typo in AreaChildrenInline.
- **2.73** — Area-admin children inline; make `geom` optional.
- **2.72** — optionally use django_extensions' ForeignKeyAutocompleteAdmin.

[Unreleased]: https://github.com/catalpainternational/simple_locations/compare/v4.2.0...dev
[4.2.0]: https://github.com/catalpainternational/simple_locations/compare/v4.1.0b2...v4.2.0
[4.0.3]: https://github.com/catalpainternational/simple_locations/compare/v4.0.2...v4.0.3
[4.0.2]: https://github.com/catalpainternational/simple_locations/compare/v4.0.0...v4.0.2
[4.0.0]: https://github.com/catalpainternational/simple_locations/releases/tag/v4.0.0
