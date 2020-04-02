"""Button module."""

from enum import Enum

from modi.module.input_module.input_module import InputModule


class Button(InputModule):

    class PropertyType(Enum):
        CLICKED = 2
        DOUBLE_CLICKED = 3
        PRESSED = 4
        TOGGLED = 5

    def __init__(self, id_, uuid, msg_send_q):
        super().__init__(id_, uuid, msg_send_q)

    def get_clicked(self):
        """
        :return: `True` if clicked or `False`.
        :rtype: bool
        """
        return self._get_property(self.PropertyType.CLICKED) == 100.0

    def get_double_clicked(self):
        """
        :return: `True` if double clicked or `False`.
        :rtype: bool
        """
        return self._get_property(self.PropertyType.DOUBLE_CLICKED) == 100.0

    def get_pressed(self):
        """
        :return: `True` if pressed or `False`.
        :rtype: bool
        """
        return self._get_property(self.PropertyType.PRESSED) == 100.0

    def get_toggled(self):
        """
        :return: `True` if toggled or `False`.
        :rtype: bool
        """
        return self._get_property(self.PropertyType.TOGGLED) == 100.0
