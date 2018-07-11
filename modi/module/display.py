# -*- coding: utf-8 -*-

"""Display module."""

from __future__ import absolute_import

from enum import Enum

from modi.module._module import OutputModule 

class PropertyType(Enum):
    CURSOR_X = 2
    CURSOR_Y = 3

class Display(OutputModule):
    property_types = PropertyType
    
    def __init__(self, id, uuid, modi):
        super(Display, self).__init__(id, uuid, modi)
        self._type = "display"
