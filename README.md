pymodi
======

<img src="https://www.gresswell.co.uk/media/catalog/product/cache/1/image/9df78eab33525d08d6e5fb8d27136e95/L/3/L308260_MODI_logo_LFC.jpg" width="500" height="150">

---------

| pyversion | distribution | documentation | coverage | maintainability | license |
|-|-|-|-|-|-|
| [![image](https://img.shields.io/pypi/pyversions/pymodi.svg)](https://pypi.python.org/pypi/pymodi) | [![image](https://img.shields.io/pypi/v/pymodi.svg)](https://pypi.python.org/pypi/pymodi) | [![Documentation Status](https://readthedocs.org/projects/pymodi/badge/?version=latest)](https://pymodi.readthedocs.io/en/latest/?badge=latest) | [![Coverage Status](https://coveralls.io/repos/github/LUXROBO/pymodi/badge.svg)](https://coveralls.io/github/LUXROBO/pymodi) | [![Maintainability](https://api.codeclimate.com/v1/badges/5a62f1585d723099e337/maintainability)](https://codeclimate.com/github/LUXROBO/pymodi/maintainability) | [![](https://img.shields.io/pypi/l/pymodi.svg?color=blue)](https://github.com/LUXROBO/pyMODI/blob/master/LICENSE) |

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

Build Status
--------

|master|develop|
|:---:|:---:|
|[![image](https://travis-ci.org/LUXROBO/pyMODI.svg?branch=master)](https://travis-ci.org/LUXROBO/pyMODI)|[![image](https://travis-ci.org/LUXROBO/pyMODI.svg?branch=develop)](https://travis-ci.org/LUXROBO/pyMODI)|

System Support
---------
| System | 3.6 | 3.7 | 3.8 |
| :---: | :---: | :---: | :--: |
| Linux | [![Build Status](https://travis-ci.org/LUXROBO/pymodi.svg?branch=master)](https://travis-ci.org/LUXROBO/pymodi) | [![Build Status](https://travis-ci.org/LUXROBO/pymodi.svg?branch=master)](https://travis-ci.org/LUXROBO/pymodi) | [![Build Status](https://travis-ci.org/LUXROBO/pymodi.svg?branch=master)](https://travis-ci.org/LUXROBO/pymodi) |
| Mac OS | [![Build Status](https://travis-ci.org/LUXROBO/pymodi.svg?branch=master)](https://travis-ci.org/LUXROBO/pymodi) | [![Build Status](https://travis-ci.org/LUXROBO/pymodi.svg?branch=master)](https://travis-ci.org/LUXROBO/pymodi) | [![Build Status](https://travis-ci.org/LUXROBO/pymodi.svg?branch=master)](https://travis-ci.org/LUXROBO/pymodi) |
| Windows | [![Build Status](https://travis-ci.org/LUXROBO/pymodi.svg?branch=master)](https://travis-ci.org/LUXROBO/pymodi) | [![Build Status](https://travis-ci.org/LUXROBO/pymodi.svg?branch=master)](https://travis-ci.org/LUXROBO/pymodi) | [![Build Status](https://travis-ci.org/LUXROBO/pymodi.svg?branch=master)](https://travis-ci.org/LUXROBO/pymodi) |

Contribution Guidelines
--------
We appreciate all contributions. If you are planning to report bugs, please do so at <https://github.com/LUXROBO/pyMODI/issues>. Feel free to fork our repository to your local environment, and please send us feedback by filing an issue.

If you want to contribute to pymodi, be sure to review the contribution guidelines. This project adheres to pymodi's code of conduct. By participating, you are expected to uphold this code.

[![Contributor Covenant](https://img.shields.io/badge/Contributor%20Covenant-v2.0%20adopted-ff69b4.svg)](CODE_OF_CONDUCT.md)

Quickstart
--------

Install the latest pyMODI if you haven\'t installed it yet:

    pip install -U pymodi --user

Import [modi]{.title-ref} package and create [MODI]{.title-ref}
instance:

    import modi
    bundle = modi.MODI(nb_modules=1)

List connected modules:

    bundle.modules

List connected LED modules and pick the first one:

    bundle.leds # List.
    bundle.leds[0] # Pick.

Let\'s blink the LED\'s light 5 times:

    import time

    led = bundle.leds[0]

    for _ in range(5):
        led.set_on()
        time.sleep(1)
        led.set_off()
        time.sleep(1)
