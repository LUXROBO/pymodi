"""Top-level package for pyMODI."""
from modi import about
from modi.modi import MODI

__all__ = ["MODI"]
__version__ = about.__version__

print(f'Running PyMODI (v{__version__})')
