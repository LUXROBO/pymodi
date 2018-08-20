# -*- coding: utf-8 -*-

"""Button module."""

from __future__ import absolute_import

from enum import Enum
from modi.module.module import InputModule

class PropertyType(Enum):
     CLICKED = 2
     DOUBLE_CLICKED = 3
     PRESSED = 4
     TOGGLED = 5

class Button(InputModule):
    """
    :param int id: The id of the module.
    :param int uuid: The uuid of the module.
    :param modi: The :class:`~modi.modi.MODI` instance.
    :type modi: :class:`~modi.modi.MODI`
    """
    property_types = PropertyType

    def __init__(self, id, uuid, modi):
        super(Button, self).__init__(id, uuid, modi)
        self._type = "button"

    def clicked(self):
        """
        :return: `True` if clicked or `False`.
        :rtype: bool
        """
        return self._properties[PropertyType.CLICKED] == 100.0

    def double_clicked(self):
        """
        :return: `True` if double clicked or `False`.
        :rtype: bool
        """
        return self._properties[PropertyType.DOUBLE_CLICKED] == 100.0

    def pressed(self):
        """
        :return: `True` if pressed or `False`.
        :rtype: bool
        """
        return self._properties[PropertyType.PRESSED] == 100.0

    def toggled(self):
        """
        :return: `True` if toggled or `False`.
        :rtype: bool
        """
        return self._properties[PropertyType.TOGGLED] == 100.0
