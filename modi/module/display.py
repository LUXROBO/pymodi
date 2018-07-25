# -*- coding: utf-8 -*-

"""Display module."""

from __future__ import absolute_import

from enum import Enum

from modi.module._module import OutputModule 

from modi._cmd import set_property
from modi._cmd import PropertyDataType

class PropertyType(Enum):
    CURSOR_X = 2
    CURSOR_Y = 3

class Display(OutputModule):
    property_types = PropertyType
    
    def __init__(self, id, uuid, modi):
        super(Display, self).__init__(id, uuid, modi)
        self._type = "display"

    def text(self, text):
        self.clear()

        for cmd in set_property(self.id, 17, text, PropertyDataType.STRING):
            self._modi().write(cmd)

    def clear(self):
        self._modi().write(set_property(self.id, 20, bytes(2), PropertyDataType.RAW))