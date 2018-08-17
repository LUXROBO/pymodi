===============
MODI Python API
===============


.. image:: https://img.shields.io/pypi/v/modi.svg
        :target: https://pypi.python.org/pypi/modi

.. image:: https://img.shields.io/pypi/pyversions/modi.svg
        :target: https://pypi.python.org/pypi/modi

.. image:: https://img.shields.io/travis/LUXROBO/MODI-Python-API.svg
        :target: https://travis-ci.org/LUXROBO/MODI-Python-API

.. image:: https://readthedocs.org/projects/modi-python-api/badge/?version=latest
        :target: https://modi-python-api.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status


.. image:: https://pyup.io/repos/github/LUXROBO/MODI-Python-API/shield.svg
     :target: https://pyup.io/repos/github/LUXROBO/MODI-Python-API/
     :alt: Updates



Easy😆 and fast💨 MODI Python API package.


* Free software: MIT license
* Documentation: https://modi-python-api.readthedocs.io.


Features
--------

* Connect to the MODI network module and control input & output modules.
* List serial ports of MODI network modules.
* Turn on or off the PnP mode of MODI modules.
* Get the position information of each modules.

Build Status
-------

master:

.. image:: https://travis-ci.org/LUXROBO/MODI-Python-API.svg?branch=master
    :target: https://travis-ci.org/LUXROBO/MODI-Python-API

develop:

.. image:: https://travis-ci.org/LUXROBO/MODI-Python-API.svg?branch=develop
    :target: https://travis-ci.org/LUXROBO/MODI-Python-API

Quickstart
-------

Install the latest MODI-Python-API if you haven't installed it yet::

        pip install -U modi

Import `modi` package and create `MODI` instance::

        import modi
        bundle = modi.MODI()

List connected modules::

        bundle.modules

List connected LED modules and pick the first one::

        bundle.leds # List.
        bundle.leds[0] # Pick.

Let's blink the LED's light 5 times::

        import time

        led = bundle.leds[0]

        for _ in range(10):
            led.on()
            time.sleep(1)
            led.off()
            time.sleep(1)

Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
