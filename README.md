<p align="center">
	<img src="https://github.com/LUXROBO/pymodi/blob/master/docs/_static/img/logo.png?raw=true" width="500" height="150">
</p>

--------
[![image](https://img.shields.io/pypi/pyversions/pymodi.svg)](https://pypi.python.org/pypi/pymodi)
[![image](https://img.shields.io/pypi/v/pymodi.svg)](https://pypi.python.org/pypi/pymodi)
[![Documentation Status](https://readthedocs.org/projects/pymodi/badge/?version=master)](https://pymodi.readthedocs.io/en/master/?badge=master)
[![Build Status](https://github.com/LUXROBO/pymodi/workflows/Build%20Status/badge.svg?branch=master)](https://github.com/LUXROBO/pymodi/actions)
![Coveralls github branch](https://img.shields.io/coveralls/github/LUXROBO/pymodi/master?style=flat-square)
[![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/LUXROBO/pymodi.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/LUXROBO/pymodi/context:python)
[![Maintainability](https://api.codeclimate.com/v1/badges/5a62f1585d723099e337/maintainability)](https://codeclimate.com/github/LUXROBO/pymodi/maintainability)
[![License](https://img.shields.io/pypi/l/pymodi.svg?color=blue)](https://github.com/LUXROBO/pymodi/blob/master/LICENSE)

Description
===========
Python API for controlling MODI.
-   Free software: MIT license
-   API Documentation: <https://pymodi.readthedocs.io>.

Promotion Video
---------------
[![pymodi](https://github.com/LUXROBO/pymodi/blob/master/docs/_static/video/pymodi-intro.gif)](https://www.youtube.com/watch?v=7ciGw8V-8sM)

Features
--------
PyMODI supports a control of modular electronics, MODI developed by [LUXROBO](https://modi.luxrobo.com/en)
* Easy control of modules through serial connection on Windows, Linux, and macOS
* Direct CAN communication to MODI modules on raspberry pi and other platforms
* Utilities of firmware update and low-level debugging of the modules

UML Diagram
-----------
<p align="center">
    <img src="https://github.com/LUXROBO/pymodi/blob/master/docs/_static/img/umldiagram.svg?raw=true">
</p>

Build Status
------------
|master|develop|
|:---:|:---:|
| [![Build Status](https://github.com/LUXROBO/pymodi/workflows/Build%20Status/badge.svg?branch=master)](https://github.com/LUXROBO/pymodi/actions) | [![Build Status](https://github.com/LUXROBO/pymodi/workflows/Build%20Status/badge.svg?branch=develop)](https://github.com/LUXROBO/pymodi/actions) |

System Support
--------------
| System | 3.6 | 3.7 | 3.8 |
| :---: | :---: | :---: | :---: |
| Linux | [![Unit Test (Ubuntu)](https://github.com/LUXROBO/pymodi/workflows/Unit%20Test%20(Ubuntu)/badge.svg?branch=master)](https://github.com/LUXROBO/pymodi/actions) | [![Unit Test (Ubuntu)](https://github.com/LUXROBO/pymodi/workflows/Unit%20Test%20(Ubuntu)/badge.svg?branch=master)](https://github.com/LUXROBO/pymodi/actions) | [![Unit Test (Ubuntu)](https://github.com/LUXROBO/pymodi/workflows/Unit%20Test%20(Ubuntu)/badge.svg?branch=master)](https://github.com/LUXROBO/pymodi/actions) |
| Mac OS | [![Unit Test (macOS)](https://github.com/LUXROBO/pymodi/workflows/Unit%20Test%20(macOS)/badge.svg?branch=master)](https://github.com/LUXROBO/pymodi/actions) | [![Unit Test (macOS)](https://github.com/LUXROBO/pymodi/workflows/Unit%20Test%20(macOS)/badge.svg?branch=master)](https://github.com/LUXROBO/pymodi/actions) | [![Unit Test (macOS)](https://github.com/LUXROBO/pymodi/workflows/Unit%20Test%20(macOS)/badge.svg?branch=master)](https://github.com/LUXROBO/pymodi/actions) |
| Windows | [![Unit Test (Windows)](https://github.com/LUXROBO/pymodi/workflows/Unit%20Test%20(Windows)/badge.svg?branch=master)](https://github.com/LUXROBO/pymodi/actions) | [![Unit Test (Windows)](https://github.com/LUXROBO/pymodi/workflows/Unit%20Test%20(Windows)/badge.svg?branch=master)](https://github.com/LUXROBO/pymodi/actions) | [![Unit Test (Windows)](https://github.com/LUXROBO/pymodi/workflows/Unit%20Test%20(Windows)/badge.svg?branch=master)](https://github.com/LUXROBO/pymodi/actions) |

Contribution Guidelines
-----------------------
We appreciate all contributions. If you are planning to report bugs, please do so [here](https://github.com/LUXROBO/pymodi/issues). Feel free to fork our repository to your local environment, and please send us feedback by filing an issue.

If you want to contribute to pymodi, be sure to review the contribution guidelines. This project adheres to pymodi's code of conduct. By participating, you are expected to uphold this code.

[![Contributor Covenant](https://img.shields.io/badge/Contributor%20Covenant-v2.0%20adopted-ff69b4.svg)](CODE_OF_CONDUCT.md)

Quickstart
----------
Install the latest PyMODI if you haven't installed it yet:
```commandline
pip install -U pymodi --user
```

You can also install PyMODI at develop branch (contains latest changes but it can be unstable) with:
```commandline
pip install git+https://github.com/LUXROBO/pymodi.git@develop --user --upgrade
```
Perhaps, you can install a stable copy of PyMODI at a specific revision, by referring a tag with:
```commandline
pip install git+https://github.com/LUXROBO/pymodi.git@v1.0.0 --user --upgrade
```
Import modi package and create MODI instance:
```python
import modi
bundle = modi.MODI()
```
List connected modules:
```python
bundle.modules
```
List connected LED modules and pick the first one:
```python
bundle.leds # List.
bundle.leds[0] # Pick.
```
Let's blink the LED's light 5 times:
```python
import time

led = bundle.leds[0]

for _ in range(5):
    # turn on for 0.5 second
    led.rgb = 255, 255, 255
    time.sleep(0.5)

    # turn off for 0.5 second
    led.rgb = 0, 0, 0
    time.sleep(0.5)
```

If you are still not sure how to use PyMODI, you can play an interactive PyMODI tutorial by running a command of
```commandline
$ python -m modi --tutorial
```
As well as an interactive usage examples:
```commandline
$ python -m modi --usage
```
Moreover, we provide some [usage and creation examples](examples), as well as a [descriptive web page](https://luxrobo.github.io/pymodi).

Usage
-----
Import modi package and create MODI instance (we call it "bundle", a bundle of MODI modules).
```python
# Import modi package
import modi

# Create MODI instance, make sure that you have connected your network module to your machine
bundle = modi.MODI()
```

However, when creating the bundle, you can specify how you would like to establish the connection between your machine and the network module.
```python
# 1. Serial connection (via USB), it's the default connection method
bundle = modi.MODI(conn_mode="ser")

# 2. BLE (Bluetooth Low Energy) connection, it's wireless! But it can be slow :(
bundle = modi.MODI(conn_mode="ble")

# 3. CAN connection (via CAN shield, not recommended to use it directly)
bundle = modi.MODI(conn_modue="can")
```

Once you created the MODI object, attach MODI modules to the network module. MODI will print what modules are connected, once they are recognized.

```python
# Create module objects given that you have attached modules below to the network module
button = bundle.buttons[0]
speaker = bundle.speakers[0]
```

To visualize how modules are connected, you can use our topology function.
```python
# Print topology map without indicating module id
bundle.print_topology_map()

# Print topology map with module id printed
bundle.print_topology_map(print_id=True)
```

Now you are ready to implement a MODI creation using PyMODI! The code below shows a simple creation using a button and a speaker module.

```python
import time

volume = 0
while True:
    speaker.tune = 880, volume
    if button.clicked:
        volume = 100 if (volume + 10) > 100 else volume + 10
        time.sleep(0.1)
    else:
        volume = 0 if (volume - 0.5) < 0 else volume - 1

    if button.double_clicked:
        break

    print(volume)
```

When implementing MODI creation with PyMODI, check [what module methods are available](https://pymodi.readthedocs.io/en/master/).

Additional Usage
----------------
To update MODI modules (all modules but the network module),
```commandline
$ python -m modi --update_module
```

To update MODI network module (the network module must be connected on serial),
```commandline
$ python -m modi --update_network_module
```

To diagnose MODI modules (helpful to find existing malfunctioning modules),
```commandline
$ python -m modi --inspect
```

To check the performance of PyMODI on your machine,
```commandline
$ python -m modi --performance
```

To see what other commands are available,
```commandline
$ python -m modi --help
```
