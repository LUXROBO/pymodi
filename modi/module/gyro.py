# -*- coding: utf-8 -*-

"""Gyro module."""

from __future__ import absolute_import

from enum import Enum

from modi.module.module import InputModule


class Gyro(InputModule):

    """
    :param int id: The id of the module.
    :param int uuid: The uuid of the module.
    :param modi: The :class:`~modi.modi.MODI` instance.
    :type modi: :class:`~modi.modi.MODI`
    """

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

    def __init__(self, module_id, uuid, modi, serial_write_q):
        super(Gyro, self).__init__(module_id, uuid, modi, serial_write_q)
        self._type = "gyro"

    def roll(self):
        """
        :return: Roll angle.
        :rtype: float
        """

        return self._get_property(self.PropertyType.ROLL)

    def pitch(self):
        """
        :return: Pitch angle.
        :rtype: float
        """

        return self._get_property(self.PropertyType.PITCH)

    def yaw(self):
        """
        :return: Yaw angle.
        :rtype: float
        """

        return self._get_property(self.PropertyType.YAW)

    def angular_vel_x(self):
        """
        :return: Angular velocity the about x-axis.
        :rtype: float
        """

        return self._get_property(self.PropertyType.ANGULAR_VEL_X)

    def angular_vel_y(self):
        """
        :return: Angular velocity the about y-axis.
        :rtype: float
        """

        return self._get_property(self.PropertyType.ANGULAR_VEL_Y)

    def angular_vel_z(self):
        """
        :return: Angular velocity the about z-axis.
        :rtype: float
        """

        return self._get_property(self.PropertyType.ANGULAR_VEL_Z)

    def acceleration_x(self):
        """
        :return: X-axis acceleration.
        :rtype: float
        """

        return self._get_property(self.PropertyType.ACCELERATION_X)

    def acceleration_y(self):
        """
        :return: Y-axis acceleration.
        :rtype: float
        """

        return self._get_property(self.PropertyType.ACCELERATION_Y)

    def acceleration_z(self):
        """
        :return: Z-axis acceleration.
        :rtype: float
        """

        return self._get_property(self.PropertyType.ACCELERATION_Z)

    def vibration(self):
        """
        :return: Vibration.
        :rtype: float
        """

        return self._get_property(self.PropertyType.VIBRATION)
