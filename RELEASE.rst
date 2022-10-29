Things to do while releasing a new version
==========================================

This file is a memo for the maintainer.


0. Checks
---------

* Check Copyright years in the About dialog
* Update screenshots
* Check screenshot links in ``linuxpkg/org.flozz.yoga-image-optimizer.metainfo.xml``


1. Release
----------

* Update version number in ``setup.py``
* Update version number in ``calcleaner/__init__.py``
* Edit / update changelog in ``README.rst``
* Add release in ``linuxpkg/org.flozz.calcleaner.metainfo.xml``
* Check appstream file: ``appstream-util validate-relax linuxpkg/org.flozz.calcleaner.metainfo.xml``
* Commit / tag (``git commit -m vX.Y.Z && git tag vX.Y.Z && git push && git push --tags``)


2. Publish PyPI package
-----------------------

Publish source dist and wheels on PyPI.

→ Automated with Github Actions :)


3. Publish Github Release
-------------------------

* Make a release on Github
* Add changelog


4. Publish the Flatpak package
------------------------------

Package repo: https://github.com/flathub/org.flozz.calcleaner

* Update commit **tag and hash** in org.flozz.calcleaner.yml
* Update dependencies (``./update-dependencies.sh``)
* Test the package:

  * Install the SDK: ``flatpak install flathub org.gnome.Sdk//43``
  * Install the runtime: ``flatpak install flathub org.gnome.Platform//43``
  * Build/install: ``flatpak-builder --force-clean --install --user build org.flozz.calcleaner.yml``
  * Run: ``flatpak run --user org.flozz.calcleaner``
  * Clean ``flatpak remove --user org.flozz.calcleaner``

* Create branch: ``git checkout -b release-vX.Y.Z && ``
* Publish: commit / tag / push: ``git commit -m vX.Y.Z && git tag vX.Y.Z && git push && git push --tags``
* Create Pull Request
* Merge Pull Request once tests passed
