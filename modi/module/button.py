# -*- coding: utf-8 -*-

"""Button module."""

from enum import Enum

from modi.module.module import InputModule


class Button(InputModule):
    """
    :param int id: The id of the module.
    :param int uuid: The uuid of the module.
    :param modi: The :class:`~modi.modi.MODI` instance.
    :type modi: :class:`~modi.modi.MODI  `
    :param serial_write_q: multiprocessing.queue of the serial writing
    """

    class PropertyType(Enum):
        CLICKED = 2
        DOUBLE_CLICKED = 3
        PRESSED = 4
        TOGGLED = 5

    def __init__(self, module_id, module_uuid, modi, serial_write_q):
        super(Button, self).__init__(module_id, module_uuid, modi, serial_write_q)
        self._module_type = "button"

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
