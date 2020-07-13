

.. raw:: html

   <p align="center">
       <img src="/docs/_static/img/logo.png" width="500" height="150">
   </p>



.. image:: https://img.shields.io/pypi/pyversions/pymodi.svg
   :target: https://pypi.python.org/pypi/pymodi
   :alt: image


.. image:: https://img.shields.io/pypi/v/pymodi.svg
   :target: https://pypi.python.org/pypi/pymodi
   :alt: image


.. image:: https://readthedocs.org/projects/pymodi/badge/?version=latest
   :target: https://pymodi.readthedocs.io/en/latest/?badge=latest
   :alt: Documentation Status


.. image:: https://github.com/LUXROBO/pymodi/workflows/Build%20Status/badge.svg?branch=master
   :target: https://github.com/LUXROBO/pymodi/actions
   :alt: Build Status


.. image:: https://coveralls.io/repos/github/LUXROBO/pymodi/badge.svg
   :target: https://coveralls.io/github/LUXROBO/pymodi
   :alt: Coverage Status


.. image:: https://api.codeclimate.com/v1/badges/5a62f1585d723099e337/maintainability
   :target: https://codeclimate.com/github/LUXROBO/pymodi/maintainability
   :alt: Maintainability


.. image:: https://img.shields.io/pypi/l/pymodi.svg?color=blue
   :target: https://github.com/LUXROBO/pymodi/blob/master/LICENSE
   :alt: License


Description
===========

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

UML Diagram
-----------


.. raw:: html

   <p align="center">
       <img src="/docs/_static/img/umldiagram.svg">
   </p>


Build Status
------------

.. list-table::
   :header-rows: 1

   * - master
     - develop
   * - 
     .. image:: https://github.com/LUXROBO/pymodi/workflows/Build%20Status/badge.svg?branch=master
        :target: https://github.com/LUXROBO/pymodi/actions
        :alt: Build Status
     
     - 
     .. image:: https://github.com/LUXROBO/pymodi/workflows/Build%20Status/badge.svg?branch=develop
        :target: https://github.com/LUXROBO/pymodi/actions
        :alt: Build Status
     


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
     .. image:: https://github.com/LUXROBO/pymodi/workflows/Unit%20Test%20(Ubuntu
        :target: https://github.com/LUXROBO/pymodi/actions
        :alt: Unit Test (Ubuntu)
     
     - 
     .. image:: https://github.com/LUXROBO/pymodi/workflows/Unit%20Test%20(Ubuntu
        :target: https://github.com/LUXROBO/pymodi/actions
        :alt: Unit Test (Ubuntu)
     
     - 
     .. image:: https://github.com/LUXROBO/pymodi/workflows/Unit%20Test%20(Ubuntu
        :target: https://github.com/LUXROBO/pymodi/actions
        :alt: Unit Test (Ubuntu)
     
   * - Mac OS
     - 
     .. image:: https://github.com/LUXROBO/pymodi/workflows/Unit%20Test%20(macOS
        :target: https://github.com/LUXROBO/pymodi/actions
        :alt: Unit Test (macOS)
     
     - 
     .. image:: https://github.com/LUXROBO/pymodi/workflows/Unit%20Test%20(macOS
        :target: https://github.com/LUXROBO/pymodi/actions
        :alt: Unit Test (macOS)
     
     - 
     .. image:: https://github.com/LUXROBO/pymodi/workflows/Unit%20Test%20(macOS
        :target: https://github.com/LUXROBO/pymodi/actions
        :alt: Unit Test (macOS)
     
   * - Windows
     - 
     .. image:: https://github.com/LUXROBO/pymodi/workflows/Unit%20Test%20(Windows
        :target: https://github.com/LUXROBO/pymodi/actions
        :alt: Unit Test (Windows)
     
     - 
     .. image:: https://github.com/LUXROBO/pymodi/workflows/Unit%20Test%20(Windows
        :target: https://github.com/LUXROBO/pymodi/actions
        :alt: Unit Test (Windows)
     
     - 
     .. image:: https://github.com/LUXROBO/pymodi/workflows/Unit%20Test%20(Windows
        :target: https://github.com/LUXROBO/pymodi/actions
        :alt: Unit Test (Windows)
     


Contribution Guidelines
-----------------------

We appreciate all contributions. If you are planning to report bugs, please do so at https://github.com/LUXROBO/pymodi/issues. Feel free to fork our repository to your local environment, and please send us feedback by filing an issue.

If you want to contribute to pymodi, be sure to review the contribution guidelines. This project adheres to pymodi's code of conduct. By participating, you are expected to uphold this code.


.. image:: https://img.shields.io/badge/Contributor%20Covenant-v2.0%20adopted-ff69b4.svg
   :target: CODE_OF_CONDUCT.md
   :alt: Contributor Covenant


Quickstart
----------

Install the latest PyMODI if you haven\'t installed it yet:

.. code-block::

   pip install -U pymodi --user


You can also install PyMODI at develop branch with:

.. code-block::

   pip install git+https://github.com/LUXROBO/pymodi.git@develop --user --upgrade


Import **modi** package and create **MODI** instance:

.. code-block::

   import modi
   bundle = modi.MODI()


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
       led.turn_on()
       time.sleep(1)
       led.turn_off()
       time.sleep(1)


If you are still not sure how to use PyMODI, you can play an interactive PyMODI tutorial by running a command of

.. code-block::

   $ python -m modi --tutorial


Moreover, we provide some `usage and creation examples. <examples>`_
