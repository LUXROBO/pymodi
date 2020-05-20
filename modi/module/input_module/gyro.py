"""Gyro module."""

from enum import Enum

from modi.module.input_module.input_module import InputModule


class Gyro(InputModule):

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

    def __init__(self, id_, uuid, msg_send_q):
        super().__init__(id_, uuid, msg_send_q)

    def get_roll(self) -> float:
        """
        :return: Roll angle.
        :rtype: float
        """

        return self._get_property(self.PropertyType.ROLL)

    def get_pitch(self) -> float:
        """
        :return: Pitch angle.
        :rtype: float
        """

        return self._get_property(self.PropertyType.PITCH)

    def get_yaw(self) -> float:
        """
        :return: Yaw angle.
        :rtype: float
        """

        return self._get_property(self.PropertyType.YAW)

    def get_angular_vel_x(self) -> float:
        """
        :return: Angular velocity the about x-axis.
        :rtype: float
        """

        return self._get_property(self.PropertyType.ANGULAR_VEL_X)

    def get_angular_vel_y(self) -> float:
        """
        :return: Angular velocity the about y-axis.
        :rtype: float
        """

        return self._get_property(self.PropertyType.ANGULAR_VEL_Y)

    def get_angular_vel_z(self) -> float:
        """
        :return: Angular velocity the about z-axis.
        :rtype: float
        """

        return self._get_property(self.PropertyType.ANGULAR_VEL_Z)

    def get_acceleration_x(self) -> float:
        """
        :return: X-axis acceleration.
        :rtype: float
        """

        return self._get_property(self.PropertyType.ACCELERATION_X)

    def get_acceleration_y(self) -> float:
        """
        :return: Y-axis acceleration.
        :rtype: float
        """

        return self._get_property(self.PropertyType.ACCELERATION_Y)

    def get_acceleration_z(self) -> float:
        """
        :return: Z-axis acceleration.
        :rtype: float
        """

        return self._get_property(self.PropertyType.ACCELERATION_Z)

    def get_vibration(self) -> float:
        """
        :return: Vibration.
        :rtype: float
        """

        return self._get_property(self.PropertyType.VIBRATION)
