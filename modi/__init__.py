"""Top-level package for pyMODI."""
from modi import about
from modi.modi import (
    MODI,
    update_module_firmware,
    update_network_firmware,
    reset_module_firmware,
    # upload_user_code,
)

__all__ = [
    "MODI",
    "update_module_firmware",
    "update_network_firmware",
    "reset_module_firmware",
    # "upload_user_code",
]

__version__ = about.__version__

print(f'Running PyMODI (v{__version__})')
