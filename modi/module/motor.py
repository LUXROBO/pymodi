# -*- coding: utf-8 -*-

"""Motor module."""

from __future__ import absolute_import

from enum import Enum

from modi.module.module import OutputModule

from modi._cmd import set_property

class PropertyType(Enum):
    FIRST_DEGREE = 4
    SECOND_DEGREE = 12
    FIRST_SPEED = 3
    SECOND_SPEED = 11
    FIRST_TORQUE = 2
    SECOND_TORQUE = 10

class Motor(OutputModule):
    property_types = PropertyType
    
    def __init__(self, id, uuid, modi):
        super(Motor, self).__init__(id, uuid, modi)
        self._type = "motor"

    def first_degree(self, degree=None):
        if degree != None:
            self._modi().write(set_property(self.id, 18, (degree, self.second_degree(), 0)))
        else:
            return self._properties[PropertyType.FIRST_DEGREE]

    def second_degree(self, degree=None):
        if degree != None:
            self._modi().write(set_property(self.id, 18, (self.first_degree(), degree, 0)))
        else:
            return self._properties[PropertyType.SECOND_DEGREE]

    def first_speed(self, speed=None):
        if speed != None:
            self._modi().write(set_property(self.id, 17, (speed, self.second_speed(), 0)))
        else:
            return self._properties[PropertyType.FIRST_SPEED]

    def second_speed(self, speed=None):
        if speed != None:
            self._modi().write(set_property(self.id, 17, (self.first_speed(), speed, 0)))
        else:    
            return self._properties[PropertyType.SECOND_SPEED]

    def first_torque(self, torque=None):
        if torque != None:
            self._modi().write(set_property(self.id, 16, (torque, self.second_torque(), 0)))
        else:
            return self._properties[PropertyType.FIRST_TORQUE]

    def second_torque(self, torque=None):
        if torque != None:
            self._modi().write(set_property(self.id, 16, (self.first_torque(), torque, 0)))
        else:
            return self._properties[PropertyType.SECOND_TORQUE]
