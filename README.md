<p align="center">
	<img src="https://github.com/LUXROBO/pymodi/blob/master/docs/_static/img/logo.png?raw=true" width="500" height="150">
</p>

--------
<div align="center">

[![Python Versions](https://img.shields.io/pypi/pyversions/pymodi.svg?style=flat-square)](https://pypi.python.org/pypi/pymodi)
[![PyPI Release (latest by date)](https://img.shields.io/github/v/release/LUXROBO/pymodi?style=flat-square)](https://pypi.python.org/pypi/pymodi)
[![Read the Docs (version)](https://img.shields.io/readthedocs/pymodi/master?style=flat-square)](https://pymodi.readthedocs.io/en/master/?badge=master)
[![GitHub Workflow Status (Build)](https://img.shields.io/github/workflow/status/LUXROBO/pymodi/Build%20Status/master?style=flat-square)](https://github.com/LUXROBO/pymodi/actions)
[![Coveralls Coverage](https://img.shields.io/coveralls/github/LUXROBO/pymodi/master?style=flat-square)](https://coveralls.io/github/LUXROBO/pymodi)
[![CodeFactor Grade](https://img.shields.io/codefactor/grade/github/LUXROBO/pymodi/master?style=flat-square)](https://www.codefactor.io/repository/github/luxrobo/pymodi/overview/master)
[![GitHub LICENSE](https://img.shields.io/github/license/LUXROBO/pymodi?style=flat-square&color=blue)](https://github.com/LUXROBO/pymodi/blob/master/LICENSE)
[![Lines of Code](https://img.shields.io/tokei/lines/github/LUXROBO/pymodi?style=flat-square)](https://github.com/LUXROBO/pymodi/tree/master/modi)

</div>

Description
===========
> Python API for controlling modular electronics, MODI.

Promotion Video
---------------
[![PyMODI Intro Video](https://github.com/LUXROBO/pymodi/blob/master/docs/_static/video/pymodi-intro.gif)](https://www.youtube.com/watch?v=7ciGw8V-8sM)

Features
--------
PyMODI provides a control of modular electronics, [MODI](https://modi.luxrobo.com/en)
* Platform agnostic control of modules through serial connection
* Explicit CAN communication to MODI modules via magnetic connector
* Utilities of wireless connection with BLE (Bluetooth Low Engery)
* Update of MODI firmware consisting of both ESP32 and STM32 modules
* Direct manipulation of MODI network module using [MODI Play](https://play.google.com/store/apps/details?id=com.luxrobo.modiplay&hl=en_US)

UML Diagram
-----------
<p align="center">
    <img src="https://github.com/LUXROBO/pymodi/blob/master/docs/_static/img/umldiagram.svg?raw=true">
</p>

Build Status
------------
|master|develop|
|:---:|:---:|
| [![GitHub Workflow Status](https://img.shields.io/github/workflow/status/LUXROBO/pymodi/Build%20Status?label=master&branch=master&logo=github&style=flat-square)](https://github.com/LUXROBO/pymodi/actions) | [![GitHub Workflow Status](https://img.shields.io/github/workflow/status/LUXROBO/pymodi/Build%20Status?label=develop&branch=develop&logo=github&style=flat-square)](https://github.com/LUXROBO/pymodi/actions)

System Support
--------------
| System | 3.6 | 3.7 | 3.8 |
| :---: | :---: | :---: | :---: |
| Linux | [![GitHub Workflow Status (branch)](https://img.shields.io/github/workflow/status/LUXROBO/pymodi/Unit%20Test%20(Ubuntu)/master?label=Unit%20Test%20%28Ubuntu%29&logo=github&style=flat-square)](https://github.com/LUXROBO/pymodi/actions) | [![GitHub Workflow Status (branch)](https://img.shields.io/github/workflow/status/LUXROBO/pymodi/Unit%20Test%20(Ubuntu)/master?label=Unit%20Test%20%28Ubuntu%29&logo=github&style=flat-square)](https://github.com/LUXROBO/pymodi/actions) |[![GitHub Workflow Status (branch)](https://img.shields.io/github/workflow/status/LUXROBO/pymodi/Unit%20Test%20(Ubuntu)/master?label=Unit%20Test%20%28Ubuntu%29&logo=github&style=flat-square)](https://github.com/LUXROBO/pymodi/actions)
| Mac OS | [![GitHub Workflow Status (branch)](https://img.shields.io/github/workflow/status/LUXROBO/pymodi/Unit%20Test%20(macOS)/master?label=Unit%20Test%20%28macOS%29&logo=github&style=flat-square)](https://github.com/LUXROBO/pymodi/actions) |[![GitHub Workflow Status (branch)](https://img.shields.io/github/workflow/status/LUXROBO/pymodi/Unit%20Test%20(macOS)/master?label=Unit%20Test%20%28macOS%29&logo=github&style=flat-square)](https://github.com/LUXROBO/pymodi/actions) | [![GitHub Workflow Status (branch)](https://img.shields.io/github/workflow/status/LUXROBO/pymodi/Unit%20Test%20(macOS)/master?label=Unit%20Test%20%28macOS%29&logo=github&style=flat-square)](https://github.com/LUXROBO/pymodi/actions)
| Windows | [![GitHub Workflow Status (branch)](https://img.shields.io/github/workflow/status/LUXROBO/pymodi/Unit%20Test%20(Windows)/master?label=Unit%20Test%20%28Windows%29&logo=github&style=flat-square)](https://github.com/LUXROBO/pymodi/actions) | [![GitHub Workflow Status (branch)](https://img.shields.io/github/workflow/status/LUXROBO/pymodi/Unit%20Test%20(Windows)/master?label=Unit%20Test%20%28Windows%29&logo=github&style=flat-square)](https://github.com/LUXROBO/pymodi/actions) | [![GitHub Workflow Status (branch)](https://img.shields.io/github/workflow/status/LUXROBO/pymodi/Unit%20Test%20(Windows)/master?label=Unit%20Test%20%28Windows%29&logo=github&style=flat-square)](https://github.com/LUXROBO/pymodi/actions)

Contribution Guidelines
-----------------------
We appreciate all contributions. If you are planning to report bugs, please do so [here](https://github.com/LUXROBO/pymodi/issues). Feel free to fork our repository to your local environment, and please send us feedback by filing an issue.

If you want to contribute to pymodi, be sure to review the contribution guidelines. This project adheres to pymodi's code of conduct. By participating, you are expected to uphold this code.

[![Contributor Covenant](https://img.shields.io/badge/Contributor%20Covenant-v2.0%20adopted-ff69b4.svg?style=flat-square)](CODE_OF_CONDUCT.md)

Installation
------------
> When installing PyMODI package, we highly recommend you to use Anaconda to manage the distribution.
> With Anaconda, you can use an isolated virtual environment, solely for PyMODI.

[Optional] Once you install [Anaconda](https://docs.anaconda.com/anaconda/install/), then:
```commandline
# Install new python environment for PyMODI package, choose python version >= 3.6
conda create --name pymodi python=3.6

# After you properly install the python environment, activate it
conda activate pymodi

# Ensure that your python version is compatible with PyMODI
python --version
```

Install the latest PyMODI if you haven't installed it yet:
```commandline
python -m pip install -U pymodi --user
```

You can also install PyMODI at develop branch (containing latest changes but it can be unstable) with:
```commandline
python -m pip install git+https://github.com/LUXROBO/pymodi.git@develop --user --upgrade
```
Alternatively, you can install a stable copy of PyMODI at a tag (representing a previous release) with:
```commandline
python -m pip install git+https://github.com/LUXROBO/pymodi.git@v1.0.0 --user --upgrade
```

Usage
-----
Import modi package and create MODI object (we call it "bundle", a bundle of MODI modules).
```python
# Import modi package
import modi

"""
Create MODI object, make sure that you have connected your network module
to your machine while other modules are attached to the network module
"""
bundle = modi.MODI()
```

[Optional] Specify how you would like to establish the connection between your machine and the network module.
```python
# 1. Serial connection (via USB), it's the default connection method
bundle = modi.MODI(conn_type="ser")

# 2. CAN connection (via CAN shield, not recommended to use it directly)
bundle = modi.MODI(conn_type="can")

# 3. BLE (Bluetooth Low Energy) connection, it's wireless! But it can be slow :(
bundle = modi.MODI(conn_type="ble", network_uuid="YOUR_NETWORK_MODULE_UUID")
```

List and create connected modules' object.
```python
# List connected modules
print(bundle.modules)

# List connected leds
print(bundle.leds)

# Pick the first led object from the bundle
led = bundle.leds[0]
```

Visualize how modules are connected.
```python
# Print topology map without indicating module id
bundle.print_topology_map()

# Print topology map with module id printed
bundle.print_topology_map(print_id=True)
```

Let's blink the LED 5 times.
```python
import time

for _ in range(5):
    # turn on for 0.5 second
    led.turn_on()
    time.sleep(0.5)

    # turn off for 0.5 second
    led.turn_off()
    time.sleep(0.5)
```

If you are still not sure how to use PyMODI, you can play PyMODI tutorial over REPL:
```commandline
$ python -m modi --tutorial
```
As well as an interactive usage examples:
```commandline
$ python -m modi --usage
```

Moreover, we provide [api documentation](https://pymodi.readthedocs.io/en/master/), [usage and creation examples](examples), and a [descriptive web page](https://luxrobo.github.io/pymodi).

Additional Usage
----------------
To update MODI network module (the network module must be connected on serial),
```commandline
$ python -m modi --update_network
```

To update MODI network module's base (as above, the network module must be connected on serial),
```commandline
$ python -m modi --update_network_base
```

To update MODI modules (all modules but the network module),
```commandline
$ python -m modi --update_modules
```

To update firmware in GUI mode (all three commands above are available)
```commandline
$ python -m modi --update_in_gui
```

To diagnose MODI modules (helpful to find existing malfunctioning modules),
```commandline
$ python -m modi --inspect
```

To debug MODI modules with PyMODI debugger,
```commandline
$ python -m modi --debug
```

To check the performance of PyMODI on your machine,
```commandline
$ python -m modi --performance
```

To initialize MODI modules implicitly (set `i` flag to enable REPL mode),
```commandline
$ python -im modi --initialize
```

To see what other commands are available,
```commandline
$ python -m modi --help
```

Sponsored by
------------
[![Ministry of SMEs and StartUps](https://github.com/LUXROBO/pymodi/blob/master/docs/_static/img/ministry_of_smes_and_startups.png?raw=true)](https://www.mss.go.kr/site/eng/main.do)
