CalCleaner
==========

|Github| |Discord| |Github Actions| |Black| |License|

    A simple graphical tool to purge old events from CalDAV calendars

.. figure:: ./screenshot.png
   :alt: Screenshot of Calcleaner

**This project is currently work in progress, it is not usable yet ;)**


Requirements
------------

Python:

* `PyGObject <https://pygobject.readthedocs.io/en/latest/>`_
* `caldav <https://github.com/python-caldav/caldav>`_

System::

    sudo apt install libgirepository1.0-dev


Hacking :)
----------

Running the project
~~~~~~~~~~~~~~~~~~~

First, install dependencies (preferably in a virtualenv)::

    pip install -e ".[dev]"

Then run::

    python -m calcleaner


Codding Style / Lint
~~~~~~~~~~~~~~~~~~~~

This project follows `Black's <https://black.readthedocs.io/en/stable/>`_ codding style.

To check codding style, you will first have to install `nox <https://nox.thea.codes/>`_::

    pip3 install nox

Then you can check for lint error (Flake8 and Black)::

    nox --session lint

You can fix automatically coding style with::

    nox -s black_fix


Tests
~~~~~

Tu run tests, you will first have to install `nox <https://nox.thea.codes/>`_::

    pip3 install nox

Then run the following command::

    nox -s test


Regenerating Icons
~~~~~~~~~~~~~~~~~~

To regenerate icons, Inkscape must be installed. On Debian and Ubuntu you can
install it with the following command::

    sudo apt install inkscape

You will also need Nox to run the generation command::

    pip3 install nox

Once everithing installed, you can regenerate icons with the following command::

    nox -s gen_icons


Supporting this project
-----------------------

Wanna support this project?

* `☕️ Buy me a coffee <https://www.buymeacoffee.com/flozz>`__,
* `❤️ sponsor me on Github <https://github.com/sponsors/flozz>`__,
* `💵️ or give me a tip on PayPal <https://www.paypal.me/0xflozz>`__.


Changelog
---------

* Nothing yet ;)


.. |Github| image:: https://img.shields.io/github/stars/flozz/calcleaner?label=Github&logo=github
   :target: https://github.com/flozz/calcleaner

.. |Discord| image:: https://img.shields.io/badge/chat-Discord-8c9eff?logo=discord&logoColor=ffffff
   :target: https://discord.gg/P77sWhuSs4

.. |Github Actions| image:: https://github.com/flozz/calcleaner/actions/workflows/python-ci.yml/badge.svg
   :target: https://github.com/flozz/calcleaner/actions

.. |Black| image:: https://img.shields.io/badge/code%20style-black-000000.svg
   :target: https://black.readthedocs.io/en/stable/

.. |License| image:: https://img.shields.io/github/license/flozz/calcleaner
   :target: https://github.com/flozz/calcleaner/blob/master/COPYING
