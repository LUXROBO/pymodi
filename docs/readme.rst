.. role:: raw-html-m2r(raw)
   :format: html


pymodi
======

:raw-html-m2r:`<img src="https://www.gresswell.co.uk/media/catalog/product/cache/1/image/9df78eab33525d08d6e5fb8d27136e95/L/3/L308260_MODI_logo_LFC.jpg" width="500" height="150">`

----

.. list-table::
   :header-rows: 1

   * - pyversion
     - distribution
     - documentation
     - coverage
     - maintainability
     - license
   * - 
     .. image:: https://img.shields.io/pypi/pyversions/pymodi.svg
        :target: https://pypi.python.org/pypi/pymodi
        :alt: image
     
     - 
     .. image:: https://img.shields.io/pypi/v/pymodi.svg
        :target: https://pypi.python.org/pypi/pymodi
        :alt: image
     
     - 
     .. image:: https://readthedocs.org/projects/pymodi/badge/?version=latest
        :target: https://pymodi.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status
     
     - 
     .. image:: https://coveralls.io/repos/github/LUXROBO/pymodi/badge.svg
        :target: https://coveralls.io/github/LUXROBO/pymodi
        :alt: Coverage Status
     
     - 
     .. image:: https://api.codeclimate.com/v1/badges/5a62f1585d723099e337/maintainability
        :target: https://codeclimate.com/github/LUXROBO/pymodi/maintainability
        :alt: Maintainability
     
     - 
     .. image:: https://img.shields.io/pypi/l/pymodi.svg?color=blue
        :target: https://github.com/LUXROBO/pyMODI/blob/master/LICENSE
        :alt: 
     


Easy😆 and fast💨 MODI Python API package.


* Free software: MIT license
* Documentation: https://pymodi.readthedocs.io.

Features
--------


* Connect to the MODI network module and control input & output
  modules.
* List serial ports of MODI network modules.
* Turn on or off the PnP mode of MODI modules.
* Get the position information of each modules.

Build Status
------------

.. list-table::
   :header-rows: 1

   * - master
     - develop
   * - 
     .. image:: https://travis-ci.org/LUXROBO/pyMODI.svg?branch=master
        :target: https://travis-ci.org/LUXROBO/pyMODI
        :alt: image
     
     - 
     .. image:: https://travis-ci.org/LUXROBO/pyMODI.svg?branch=develop
        :target: https://travis-ci.org/LUXROBO/pyMODI
        :alt: image
     


System Support
--------------

.. list-table::
   :header-rows: 1

   * - System
     - 3.6
     - 3.7
     - 3.8
   * - Linux
     - 
     .. image:: https://travis-ci.org/LUXROBO/pymodi.svg?branch=master
        :target: https://travis-ci.org/LUXROBO/pymodi
        :alt: Build Status
     
     - 
     .. image:: https://travis-ci.org/LUXROBO/pymodi.svg?branch=master
        :target: https://travis-ci.org/LUXROBO/pymodi
        :alt: Build Status
     
     - 
     .. image:: https://travis-ci.org/LUXROBO/pymodi.svg?branch=master
        :target: https://travis-ci.org/LUXROBO/pymodi
        :alt: Build Status
     
   * - Mac OS
     - 
     .. image:: https://travis-ci.org/LUXROBO/pymodi.svg?branch=master
        :target: https://travis-ci.org/LUXROBO/pymodi
        :alt: Build Status
     
     - 
     .. image:: https://travis-ci.org/LUXROBO/pymodi.svg?branch=master
        :target: https://travis-ci.org/LUXROBO/pymodi
        :alt: Build Status
     
     - 
     .. image:: https://travis-ci.org/LUXROBO/pymodi.svg?branch=master
        :target: https://travis-ci.org/LUXROBO/pymodi
        :alt: Build Status
     
   * - Windows
     - 
     .. image:: https://travis-ci.org/LUXROBO/pymodi.svg?branch=master
        :target: https://travis-ci.org/LUXROBO/pymodi
        :alt: Build Status
     
     - 
     .. image:: https://travis-ci.org/LUXROBO/pymodi.svg?branch=master
        :target: https://travis-ci.org/LUXROBO/pymodi
        :alt: Build Status
     
     - 
     .. image:: https://travis-ci.org/LUXROBO/pymodi.svg?branch=master
        :target: https://travis-ci.org/LUXROBO/pymodi
        :alt: Build Status
     


Contribution Guidelines
-----------------------

We appreciate all contributions. If you are planning to report bugs, please do so at https://github.com/LUXROBO/pyMODI/issues. Feel free to fork our repository to your local environment, and please send us feedback by filing an issue.

If you want to contribute to pymodi, be sure to review the contribution guidelines. This project adheres to pymodi's code of conduct. By participating, you are expected to uphold this code.


.. image:: https://img.shields.io/badge/Contributor%20Covenant-v2.0%20adopted-ff69b4.svg
   :target: CODE_OF_CONDUCT.md
   :alt: Contributor Covenant


Quickstart
----------

Install the latest pyMODI if you haven\'t installed it yet:

.. code-block::

   pip install -U pymodi --user


Import [modi]{.title-ref} package and create [MODI]{.title-ref}
instance:

.. code-block::

   import modi
   bundle = modi.MODI(nb_modules=1)


List connected modules:

.. code-block::

   bundle.modules


List connected LED modules and pick the first one:

.. code-block::

   bundle.leds # List.
   bundle.leds[0] # Pick.


Let\'s blink the LED\'s light 5 times:

.. code-block::

   import time

   led = bundle.leds[0]

   for _ in range(5):
       led.set_on()
       time.sleep(1)
       led.set_off()
       time.sleep(1)
