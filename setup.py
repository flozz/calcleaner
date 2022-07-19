#!/usr/bin/env python
# encoding: UTF-8

import os

from setuptools import setup, find_packages


long_description = ""
if os.path.isfile("README.rst"):
    long_description = open("README.rst", "r", encoding="UTF-8").read()


setup(
    name="calcleaner",
    version="0.0.0",
    description="A simple graphical tool to purge old events from CalDAV calendars",
    url="https://github.com/flozz/calcleaner",
    license="GPLv3",
    long_description=long_description,
    keywords="calendar caldav event cleaner purge prune",
    author="Fabien LOISON",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "caldav>=0.9.1",
        "PyGObject>=3.26",
    ],
    extras_require={
        "dev": [
            "nox",
            "flake8",
            "black",
            "pytest",
        ]
    },
    entry_points={
        "console_scripts": [
            "calcleaner = calcleaner.__main__:main",
        ]
    },
)
