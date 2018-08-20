# -*- coding: utf-8 -*-

"""Display module."""

from __future__ import absolute_import

from enum import Enum

from modi.module.module import OutputModule 

from modi._cmd import set_property
from modi._cmd import PropertyDataType

class PropertyType(Enum):
    CURSOR_X = 2
    CURSOR_Y = 3

class Display(OutputModule):
    """
    :param int id: The id of the module.
    :param int uuid: The uuid of the module.
    :param modi: The :class:`~modi.modi.MODI` instance.
    :type modi: :class:`~modi.modi.MODI`
    """
    property_types = PropertyType
    
    def __init__(self, id, uuid, modi):
        super(Display, self).__init__(id, uuid, modi)
        self._type = "display"

    def text(self, text):
        """
        :param text: Text to display.
        """
        self.clear()

        for cmd in set_property(self.id, 17, text, PropertyDataType.STRING):
            self._modi().write(cmd)

    def clear(self):
        """Clear the screen.
        """
        self._modi().write(set_property(self.id, 20, bytes(2), PropertyDataType.RAW))
