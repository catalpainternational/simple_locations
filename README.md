## simple_locations

The common location package used for catalpa's projects. A hierarchical tree of geographical locations supporting location type and GIS data.

## Admin

The admin site is set up to use Modeltranslations (if available in the parent app)

For modeltranslations, please remember to run `sync_translation_fields` in order to get `name_en`, `name_tet` etc. fields.


## Environment

This is intended to be compatible with:
 - Django 3.1, 3.2, 4.0
 - Python 3.7, 3.8, 3.9

```sh
gh repo clone catalpainternational/simple_locations
cd simple_locations
python -m venv env
. env/bin/activate
pip install pip-tools
pip-sync requirements.txt dev.txt
pre-commit install
```

#### Changelog

  * Version 3.0
    - Code style changes (black, flake8) and

  * Version 2.77
    - first pass of updates for Python 3.8+ and Django 3.1+

  * Version 2.75
    - add modeltranslations

  * Version 2.74
    - fix CORS issue breaking maps in AreaAdmin
    - typo in AreaChildrenInline

  * Version 2.73
    - add an inline showing children to the Area admin
    - make the `geom` field optional

  * Version 2.72
    - optionally use django_extensions' ForeignKeyAutocompleteAdmin in admin interface


##### Uploading a new version to PyPi

* install setuptools and twine
* Bump `setup.py` to a new version
*
* Create a git tag for this version: `git tag <version_number>`
* Push the tag to github `git push origin <version_number>`
* Upload the new version to PyPi: `python setup.py sdist upload`


If you have pipenv:
```
pipenv install
```

```
# bump setup.py then:
pipenv run python setup.py sdist bdist_wheel
pipenv run twine upload dist/*
rm -rf dist/*
```
