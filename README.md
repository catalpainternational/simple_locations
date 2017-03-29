#### Uploading a new version to PyPi

* Bump `setup.py` to a new version
* Create a git tag for this version: `git tag <version_number>`
* Push the tag to github `git push origin <version_number>`
* Upload the new version to PyPi: `python setup.py sdist upload`
