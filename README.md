#### Uploading a new version to PyPi

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
