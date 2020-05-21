"""Top-level package for pyMODI."""
from modi.modi import MODI
from os import path

__all__ = ["MODI"]

about = {}
here = path.dirname(__file__)
with open(path.join(here, '..', 'about.py')) as about_file:
    exec(about_file.read(), about)

__version__ = about['__version__']
