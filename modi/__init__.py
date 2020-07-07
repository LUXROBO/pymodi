"""Top-level package for pyMODI."""

from modi.modi import MODI
from modi import about

__all__ = ["MODI"]
__version__ = about.__version__

# Check PyMODI version
import json
import urllib.request as ur
from urllib.error import URLError

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
