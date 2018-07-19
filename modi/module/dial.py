# -*- coding: utf-8 -*-

"""Dial module."""

from __future__ import absolute_import

from enum import Enum

from modi.module._module import InputModule

class PropertyType(Enum):
    DEGREE = 2 

class Dial(InputModule):
    property_types = PropertyType
    
    def __init__(self, id, uuid, modi):
        super(Dial, self).__init__(id, uuid, modi)
        self._type = "dial"

    def degree(self):
        return self._properties[PropertyType.DEGREE]