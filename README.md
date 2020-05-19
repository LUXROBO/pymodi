pymodi
======
| pyversion | distribution | documentation | coverage | maintainability | license |
|-|-|-|-|-|-|
| [![image](https://img.shields.io/pypi/pyversions/pymodi.svg)](https://pypi.python.org/pypi/pymodi) | [![image](https://img.shields.io/pypi/v/pymodi.svg)](https://pypi.python.org/pypi/pymodi) | [![Documentation Status](https://readthedocs.org/projects/pymodi/badge/?version=latest)](https://pymodi.readthedocs.io/en/latest/?badge=latest) | [![Coverage Status](https://coveralls.io/repos/github/LUXROBO/pymodi/badge.svg)](https://coveralls.io/github/LUXROBO/pymodi) | [![Maintainability](https://api.codeclimate.com/v1/badges/3e5f0248ac50d580cb3f/maintainability)](https://codeclimate.com/github/LUXROBO/pyMODI/maintainability) | [![](https://img.shields.io/pypi/l/pymodi.svg?color=blue)](https://github.com/LUXROBO/pyMODI/blob/master/LICENSE) |

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
