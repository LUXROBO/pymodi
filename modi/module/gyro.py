# -*- coding: utf-8 -*-

"""Gyro module."""

from __future__ import absolute_import

from enum import Enum

from modi.module._module import InputModule

class PropertyType(Enum):
    ROLL = 2
    PITCH = 3
    YAW = 4
    ANGULAR_VEL_X = 5
    ANGULAR_VEL_Y = 6
    ANGULAR_VEL_Z = 7
    ACCELERATION_X = 8
    ACCELERATION_Y = 9
    ACCELERATION_Z = 10
    VIBRATION = 11

class Gyro(InputModule):
    property_types = PropertyType
    
    def __init__(self, id, uuid, modi):
        super(Gyro, self).__init__(id, uuid, modi)
        self._type = "gyro"

    def roll(self):
        return self._properties[PropertyType.ROLL]

    def pitch(self):
        return self._properties[PropertyType.PITCH]

    def yaw(self):
        return self._properties[PropertyType.YAW]

    def angular_vel_x(self):
        return self._properties[PropertyType.ANGULAR_VEL_X]

    def angular_vel_y(self):
        return self._properties[PropertyType.ANGULAR_VEL_Y]

    def angular_vel_z(self):
        return self._properties[PropertyType.ANGULAR_VEL_Z]

    def acceleration_x(self):
        return self._properties[PropertyType.ACCELERATION_X]

    def acceleration_y(self):
        return self._properties[PropertyType.ACCELERATION_Y]

    def acceleration_z(self):
        return self._properties[PropertyType.ACCELERATION_Z]

    def vibration(self):
        return self._properties[PropertyType.VIBRATION]
