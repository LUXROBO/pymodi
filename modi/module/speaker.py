# -*- coding: utf-8 -*-

"""Speaker module."""

from __future__ import absolute_import

from enum import Enum

from modi.module._module import OutputModule

class PropertyType(Enum):
    FREQUENCY = 3
    VOLUME = 2

class Speaker(OutputModule):
    property_types = PropertyType
    
    def __init__(self, id, uuid, modi):
        super(Speaker, self).__init__(id, uuid, modi)
        self._type = "speaker"

    def frequency(self):
        return self._properties[PropertyType.FREQUENCY]

    def volume(self):
        return self._properties[PropertyType.VOLUME]