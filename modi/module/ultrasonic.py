# -*- coding: utf-8 -*-

"""Ultrasonic module."""

from __future__ import absolute_import

from enum import Enum

from modi.module._module import InputModule

class PropertyType(Enum):
    DISTANCE = 2

class Ultrasonic(InputModule):
    property_types = PropertyType

    def __init__(self, id, uuid, modi):
        super(Ultrasonic, self).__init__(id, uuid, modi)
        self._type = "ultrasonic"

    def distance(self):
        return self._properties[PropertyType.DISTANCE]