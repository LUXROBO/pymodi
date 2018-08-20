# -*- coding: utf-8 -*-

"""Mic module."""

from __future__ import absolute_import

from enum import Enum

from modi.module.module import InputModule

class PropertyType(Enum):
    VOLUME = 2
    FREQUENCY = 3

class Mic(InputModule):
    property_types = PropertyType
    
    def __init__(self, id, uuid, modi):
        super(Mic, self).__init__(id, uuid, modi)
        self._type = "mic"

    def volume(self):
        return self._properties[PropertyType.VOLUME]

    def frequency(self):
        return self._properties[PropertyType.FREQUENCY]
