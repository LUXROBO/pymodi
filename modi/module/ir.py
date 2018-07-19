# -*- coding: utf-8 -*-

"""IR module."""

from __future__ import absolute_import

from enum import Enum

from modi.module._module import InputModule

class PropertyType(Enum):
    DISTANCE = 2
    BRIGHTNESS = 3

class Ir(InputModule):
    property_types = PropertyType

    def __init__(self, id, uuid, modi):
        super(Ir, self).__init__(id, uuid, modi)
        self._type = "ir"

    def distance(self):
        return self._properties[PropertyType.DISTANCE]

    def brightness(self):
        return self._properties[PropertyType.BRIGHTNESS]