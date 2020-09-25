<p align="center">
	<img src="https://github.com/LUXROBO/pymodi/blob/master/docs/_static/img/logo.png?raw=true" width="500" height="150">
</p>

--------
<div align="center">

[![image](https://img.shields.io/pypi/pyversions/pymodi.svg?style=flat-square)](https://pypi.python.org/pypi/pymodi)
[![GitHub release (latest by date)](https://img.shields.io/github/v/release/LUXROBO/pymodi?style=flat-square)](https://pypi.python.org/pypi/pymodi)
[![Read the Docs (version)](https://img.shields.io/readthedocs/pymodi/master?style=flat-square)](https://pymodi.readthedocs.io/en/master/?badge=master)
[![GitHub Workflow Status (branch)](https://img.shields.io/github/workflow/status/LUXROBO/pymodi/Build%20Status/master?style=flat-square)](https://github.com/LUXROBO/pymodi/actions)
[![Coveralls github branch](https://img.shields.io/coveralls/github/LUXROBO/pymodi/master?style=flat-square)](https://coveralls.io/github/LUXROBO/pymodi)
[![CodeFactor Grade](https://img.shields.io/codefactor/grade/github/LUXROBO/pymodi/master?style=flat-square)](https://www.codefactor.io/repository/github/luxrobo/pymodi/overview/master)
[![GitHub](https://img.shields.io/github/license/LUXROBO/pymodi?style=flat-square&color=blue)](https://github.com/LUXROBO/pymodi/blob/master/LICENSE)
[![Lines of code](https://img.shields.io/tokei/lines/github/LUXROBO/pymodi?style=flat-square)](https://github.com/LUXROBO/pymodi/tree/master/modi)

</div>

Description
===========
> Python API for controlling modular electronics, MODI.

Promotion Video
---------------
[![pymodi](https://github.com/LUXROBO/pymodi/blob/master/docs/_static/video/pymodi-intro.gif)](https://www.youtube.com/watch?v=7ciGw8V-8sM)

Features
--------
PyMODI supports a control of modular electronics, [MODI](https://modi.luxrobo.com/en)
* Easy control of modules through different types of connections on Windows, Linux, and macOS
* Direct CAN communication to MODI modules on raspberry pi and other platforms
* Utilities of MODI firmware update and low-level debugging of the modules

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
> When installing PyMODI package, we highly recommend you to use Anaconda to manage the distribution. With Anaconda, you can use an isolated virtual environment for PyMODI.

[Optional] Once you install [Anaconda](https://docs.anaconda.com/anaconda/install/), then:
```commandline
# Install new python environment for PyMODI package, choose python version >= 3.6
conda create --name pymodi python=3.6

# Make sure that your python's version is compatible with PyMODI
python --version

# After you properly install the python environment, activate it
conda activate pymodi
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

# Create MODI object, make sure that you have connected your network module to your machine with other modules attached to it
bundle = modi.MODI()
```

You can optionally specify how you would like to establish the connection between your machine and the network module.
```python
# 1. Serial connection (via USB), it's the default connection method
bundle = modi.MODI(conn_mode="ser")

# 2. CAN connection (via CAN shield, not recommended to use it directly)
bundle = modi.MODI(conn_modue="can")

# 3. BLE (Bluetooth Low Energy) connection, it's wireless! But it can be slow :(
bundle = modi.MODI(conn_mode="ble", uuid="YOUR_NETWORK_MODULE_UUID")
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
    led.rgb = 255, 255, 255
    time.sleep(0.5)

    # turn off for 0.5 second
    led.rgb = 0, 0, 0
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

To automatically initialize MODI modules, useful for debugging (set `i` flag to enable REPL mode),
```commandline
$ python -im modi --debug
```

To see what other commands are available,
```commandline
$ python -m modi --help
```

Sponsored by
------------
[![ministry of smes and startups](https://gtihub.com/LUXROBO/pymodi/blob/master/docs/_static/img/smes_startups.png?raw=true)](https://www.mss.go.kr/site/eng/main.do)
