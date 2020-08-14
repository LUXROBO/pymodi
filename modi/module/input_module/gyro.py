"""Gyro module."""

from modi.module.input_module.input_module import InputModule


class Gyro(InputModule):

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

    @property
    def roll(self) -> float:
        """Returns the roll angle of the gyro

        :return: Roll angle.
        :rtype: float
        """

        return self._get_property(Gyro.ROLL)

    @property
    def pitch(self) -> float:
        """Returns the pitch angle of the gyro

        :return: Pitch angle.
        :rtype: float
        """

        return self._get_property(Gyro.PITCH)

    @property
    def yaw(self) -> float:
        """Returns the yaw angle of the gyro

        :return: Yaw angle.
        :rtype: float
        """

        return self._get_property(Gyro.YAW)

    @property
    def angular_vel_x(self) -> float:
        """Returns the roll angle of the gyro

        :return: Angular velocity the about x-axis.
        :rtype: float
        """

        return self._get_property(Gyro.ANGULAR_VEL_X)

    @property
    def angular_vel_y(self) -> float:
        """Returns the angular velocity about y-axis

        :return: Angular velocity the about y-axis.
        :rtype: float
        """

        return self._get_property(Gyro.ANGULAR_VEL_Y)

    @property
    def angular_vel_z(self) -> float:
        """Returns the angular velocity about z-axis

        :return: Angular velocity the about z-axis.
        :rtype: float
        """

        return self._get_property(Gyro.ANGULAR_VEL_Z)

    @property
    def acceleration_x(self) -> float:
        """Returns the x component of the acceleration

        :return: X-axis acceleration.
        :rtype: float
        """

        return self._get_property(Gyro.ACCELERATION_X)

    @property
    def acceleration_y(self) -> float:
        """Returns the y component of the acceleration

        :return: Y-axis acceleration.
        :rtype: float
        """

        return self._get_property(Gyro.ACCELERATION_Y)

    @property
    def acceleration_z(self) -> float:
        """Returns the z component of the acceleration

        :return: Z-axis acceleration.
        :rtype: float
        """

        return self._get_property(Gyro.ACCELERATION_Z)

    @property
    def vibration(self) -> float:
        """Returns the vibration value

        :return: Vibration.
        :rtype: float
        """

        return self._get_property(Gyro.VIBRATION)
