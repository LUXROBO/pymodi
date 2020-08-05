"""Top-level package for pyMODI."""

import json

import urllib.request as ur

from multiprocessing import current_process
from sys import version_info
from urllib.error import URLError

from modi import about
from modi.modi import MODI

__all__ = ["MODI"]
__version__ = about.__version__


if "Main" in current_process().name:
    print(f'Running PyMODI (v{__version__})')

    try:
        # Check PyMODI version
        url = "https://pypi.org/pypi/pymodi/json"
        pypi_pymodi_data = json.load(ur.urlopen(url, timeout=1))
        latest_pymodi_version = list(pypi_pymodi_data["releases"].keys())[-1]
        if __version__ != latest_pymodi_version:
            print(f"Newer PyMODI (v{latest_pymodi_version}) is available!")

        # Check python version
        major, minor, micro, = (
            version_info.major, version_info.minor, version_info.micro
        )
        pypi_minors = [
            int(c.split('.')[1]) for c in
            pypi_pymodi_data['info']['classifiers'] if
            c.startswith('Programming Language :: Python :: 3.')
        ]
        if major != 3 or not (min(pypi_minors) <= minor <= max(pypi_minors)):
            raise Exception(f"Latest PyMODI does not support "
                            f"running python version {major}.{minor}.{micro}")
    except URLError:
        print(f"Cannot validate running PyMODI(v{__version__}), "
              "please check your internet connection")
