CalCleaner
==========

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

Codding Style / Lint
~~~~~~~~~~~~~~~~~~~~

This project follows `Black's <https://black.readthedocs.io/en/stable/>`_ codding style.

To check codding style, you will first have to install `nox <https://nox.thea.codes/>`_::

    pip3 install nox

Then you can check for lint error (Flake8 and Black)::

    nox --session lint

You can fix automatically coding style with::

    nox -s black_fix

Running the project
~~~~~~~~~~~~~~~~~~~

First, install dependencies (preferably in a virtualenv)::

    pip install -e ".[dev]"

Then run::

    python -m calcleaner


Supporting this project
-----------------------

Wanna support this project?

* `☕️ Buy me a coffee <https://www.buymeacoffee.com/flozz>`__,
* `❤️ sponsor me on Github <https://github.com/sponsors/flozz>`__,
* `💵️ or give me a tip on PayPal <https://www.paypal.me/0xflozz>`__.


Changelog
---------

* Nothing yet ;)
