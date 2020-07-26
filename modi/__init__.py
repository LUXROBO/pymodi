"""Top-level package for pyMODI."""

import json

import urllib.request as ur

from sys import version_info
from urllib.error import URLError
from multiprocessing import current_process

from modi.modi import MODI
from modi import about

__all__ = ["MODI"]
__version__ = about.__version__

# Check PyMODI version
if "Main" in current_process().name:
    print(f'Running PyMODI (v{__version__})')

    try:
        url = "https://pypi.org/pypi/pymodi/json"
        pypi_pymodi_data = json.load(ur.urlopen(url))
        latest_pymodi_version = list(pypi_pymodi_data["releases"].keys())[-1]
        if __version__ != latest_pymodi_version:
            print(f"Newer PyMODI (v{latest_pymodi_version}) is available!")
    except URLError:
        print("Cannot check the latest version of PyMODI, "
              "please check your internet connection")

# Check python version
major, minor, micro, = (
    version_info.major, version_info.minor, version_info.micro
)
if major != 3 or not (6 < minor < 8):
    raise Exception(f"PyMODI (v{__version__}) does not support "
                    f"current python version {major}.{minor}.{micro}")
