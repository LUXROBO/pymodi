<p align="center">
	<img src="docs/_static/img/logo.png" width="500" height="150">
</p>


[![image](https://img.shields.io/pypi/pyversions/pymodi.svg)](https://pypi.python.org/pypi/pymodi)
[![image](https://img.shields.io/pypi/v/pymodi.svg)](https://pypi.python.org/pypi/pymodi)
[![Documentation Status](https://readthedocs.org/projects/pymodi/badge/?version=latest)](https://pymodi.readthedocs.io/en/latest/?badge=latest)
[![Build Status](https://github.com/LUXROBO/pymodi/workflows/Build%20Status/badge.svg?branch=master)](https://github.com/LUXROBO/pymodi/actions)
[![Coverage Status](https://coveralls.io/repos/github/LUXROBO/pymodi/badge.svg)](https://coveralls.io/github/LUXROBO/pymodi)
[![Maintainability](https://api.codeclimate.com/v1/badges/5a62f1585d723099e337/maintainability)](https://codeclimate.com/github/LUXROBO/pymodi/maintainability)
[![License](https://img.shields.io/pypi/l/pymodi.svg?color=blue)](https://github.com/LUXROBO/pymodi/blob/master/LICENSE)

Description
=========
Easy😆 and fast💨 MODI Python API package.

-   Free software: MIT license
-   Documentation: <https://pymodi.readthedocs.io>.

Features
--------
-   Connect to the MODI network module and control input & output
    modules.
-   List serial ports of MODI network modules.
-   Turn on or off the PnP mode of MODI modules.
-   Get the position information of each modules.

UML Diagram
--------
<p align="center">
    <img src="/docs/_static/img/umldiagram.svg">
</p>

Build Status
--------

|master|develop|
|:---:|:---:|
| [![Build Status](https://github.com/LUXROBO/pymodi/workflows/Build%20Status/badge.svg?branch=master)](https://github.com/LUXROBO/pymodi/actions) | [![Build Status](https://github.com/LUXROBO/pymodi/workflows/Build%20Status/badge.svg?branch=develop)](https://github.com/LUXROBO/pymodi/actions) |

System Support
---------
| System | 3.6 | 3.7 | 3.8 |
| :---: | :---: | :---: | :--: |
| Linux | [![Unit Test (Ubuntu)](https://github.com/LUXROBO/pymodi/workflows/Unit%20Test%20(Ubuntu)/badge.svg?branch=master)](https://github.com/LUXROBO/pymodi/actions) | [![Unit Test (Ubuntu)](https://github.com/LUXROBO/pymodi/workflows/Unit%20Test%20(Ubuntu)/badge.svg?branch=master)](https://github.com/LUXROBO/pymodi/actions) | [![Unit Test (Ubuntu)](https://github.com/LUXROBO/pymodi/workflows/Unit%20Test%20(Ubuntu)/badge.svg?branch=master)](https://github.com/LUXROBO/pymodi/actions) |
| Mac OS | [![Unit Test (macOS)](https://github.com/LUXROBO/pymodi/workflows/Unit%20Test%20(macOS)/badge.svg?branch=master)](https://github.com/LUXROBO/pymodi/actions) | [![Unit Test (macOS)](https://github.com/LUXROBO/pymodi/workflows/Unit%20Test%20(macOS)/badge.svg?branch=master)](https://github.com/LUXROBO/pymodi/actions) | [![Unit Test (macOS)](https://github.com/LUXROBO/pymodi/workflows/Unit%20Test%20(macOS)/badge.svg?branch=master)](https://github.com/LUXROBO/pymodi/actions) |
| Windows | [![Unit Test (Windows)](https://github.com/LUXROBO/pymodi/workflows/Unit%20Test%20(Windows)/badge.svg?branch=master)](https://github.com/LUXROBO/pymodi/actions) | [![Unit Test (Windows)](https://github.com/LUXROBO/pymodi/workflows/Unit%20Test%20(Windows)/badge.svg?branch=master)](https://github.com/LUXROBO/pymodi/actions) | [![Unit Test (Windows)](https://github.com/LUXROBO/pymodi/workflows/Unit%20Test%20(Windows)/badge.svg?branch=master)](https://github.com/LUXROBO/pymodi/actions) |

Contribution Guidelines
--------
We appreciate all contributions. If you are planning to report bugs, please do so at <https://github.com/LUXROBO/pymodi/issues>. Feel free to fork our repository to your local environment, and please send us feedback by filing an issue.

If you want to contribute to pymodi, be sure to review the contribution guidelines. This project adheres to pymodi's code of conduct. By participating, you are expected to uphold this code.

[![Contributor Covenant](https://img.shields.io/badge/Contributor%20Covenant-v2.0%20adopted-ff69b4.svg)](CODE_OF_CONDUCT.md)

Quickstart
--------

Install the latest PyMODI if you haven\'t installed it yet:

    pip install -U pymodi --user

You can also install PyMODI at develop branch with:

    pip install git+https://github.com/LUXROBO/pymodi.git@develop --user --upgrade

Import **modi** package and create **MODI** instance:

    import modi
    bundle = modi.MODI()

List connected modules:

    bundle.modules

List connected LED modules and pick the first one:

    bundle.leds # List.
    bundle.leds[0] # Pick.

Let\'s blink the LED\'s light 5 times:

    import time

    led = bundle.leds[0]

    for _ in range(5):
        led.turn_on()
        time.sleep(1)
        led.turn_off()
        time.sleep(1)

If you are still not sure how to use PyMODI, you can play an interactive PyMODI tutorial by running a command of

    $ python -m modi --tutorial

Moreover, we provide some [usage and creation examples.](examples)
