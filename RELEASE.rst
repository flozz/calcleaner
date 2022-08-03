Things to do while releasing a new version
==========================================

This file is a memo for the maintainer.


1. Release
----------

* Update version number in ``setup.py``
* Update version number in ``calcleaner/__init__.py``
* Update version number in ``linuxpkg/org.flozz.calcleaner.metainfo``
* Edit / update changelog in ``README.rst``
* Commit / tag (``git commit -m vX.Y.Z && git tag vX.Y.Z && git push && git push --tags``)


2. Publish PyPI package
-----------------------

Publish source dist and wheels on PyPI.

TODO: automate with Github Actions

::

    pip install wheel twine
    nox -s locales_compile
    python3 setup.py sdist bdist_wheel
    twine upload dist/*


3. Publish Github Release
~~~~~~~~~~~~~~~~~~~~~~~~~

* Make a release on Github
* Add changelog
