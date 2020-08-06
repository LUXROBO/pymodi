"""Network module."""

from enum import IntEnum

from modi.module.setup_module.setup_module import SetupModule


class Battery(SetupModule):
    class PropertyType(IntEnum):
        RESERVED = 0
