## simple_locations

The common location package used for catalpa's projects. A hierarchical tree of geographical locations supporting location type and GIS data

#### Changelog

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
