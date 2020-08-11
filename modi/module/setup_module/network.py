"""Network module."""

from enum import IntEnum

from modi.module.setup_module.setup_module import SetupModule


class Network(SetupModule):
    class PropertyType(IntEnum):
        BUTTON = 3

    @property
    def button_pressed(self):
        return self._get_property(self.PropertyType.BUTTON)
