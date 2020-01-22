# -*- coding: utf-8 -*-

"""Motor module."""

from __future__ import absolute_import

from enum import Enum

from modi.module.module import OutputModule


class Motor(OutputModule):
    """
    :param int id: The id of the module.
    :param int uuid: The uuid of the module.
    :param modi: The :class:`~modi.modi.MODI` instance.
    :type modi: :class:`~modi.modi.MODI`
    """

    class PropertyType(Enum):
        FIRST_TORQUE = 2
        SECOND_TORQUE = 10
        FIRST_SPEED = 3
        SECOND_SPEED = 11
        FIRST_DEGREE = 4
        SECOND_DEGREE = 12

    class ControlType(Enum):
        TORQUE = 16
        SPEED = 17
        DEGREE = 18
        INV = 19

    def __init__(self, id, uuid, modi, serial_write_q):
        super(Motor, self).__init__(id, uuid, modi, serial_write_q)
        self._type = "motor"
        self._serial_write_q = serial_write_q

    def motor_ch_ctrl(self, channel, mode, value=None):
        """
        Channel: 0/1 -> Top/Bot
        Mode: 0/1/2 -> Torque, Speed, Angle (Torque is not implemented yet)
        """
        if value is not None:
            self._serial_write_q.put(
                self._command.set_property(
                    self.id,
                    self.ControlType.INV.value,
                    (channel, mode, value, 0x00 if value >= 0 else 0xFFFF),
                )
            )
        # TODO: implement return statement below
        # return (
        #    self._get_property(self.PropertyType.?),
        #    self._get_property(self.PropertyType.?),
        # )

    def first_degree(self, degree=None):
        """
        :param int degree: Angle to set the first motor.

        If *degree* is ``None``,

        :return: Angle of the first motor.
        :rtype: float
        """
        if degree is not None:
            self._serial_write_q.put(
                self._command.set_property(
                    self.id,
                    self.ControlType.DEGREE.value,
                    (degree, self._get_property(self.PropertyType.FIRST_DEGREE), 0),
                )
            )
        else:
            return self._get_property(self.PropertyType.FIRST_DEGREE)

    def second_degree(self, degree=None):
        """
        :param int degree: Angle to set the second motor.

        If *degree* is ``None``,

        :return: Angle of the second motor.
        :rtype: float
        """
        if degree is not None:
            self._serial_write_q.put(
                self._command.set_property(
                    self.id, self.ControlType.DEGREE, (self.second_degree(), degree, 0)
                )
            )
        else:
            return self._get_property(self.PropertyType.SECOND_DEGREE)

    def first_speed(self, speed=None):
        """
        :param int degree: Angular speed to set the first motor.

        If *speed* is ``None``,

        :return: Angular speed of the first motor.
        :rtype: float
        """
        if speed is not None:
            self._serial_write_q.put(
                self._command.set_property(
                    self.id,
                    self.ControlType.SPEED.value,
                    (speed, self.first_speed(), 0),
                )
            )
        else:
            return self._get_property(self.PropertyType.FIRST_DEGREE)

    def second_speed(self, speed=None):
        """
        :param int degree: Angular speed to set the second motor.

        If *speed* is ``None``,

        :return: Angular speed of the second motor.
        :rtype: float
        """
        if speed is not None:
            self._serial_write_q.put(
                self._command.set_property(
                    self.id,
                    self.ControlType.SPEED.value,
                    (self.second_speed(), speed, 0),
                )
            )
        else:
            return self._get_property(self.PropertyType.SECOND_DEGREE)

    def first_torque(self, torque=None):
        """
        :param int degree: Torque to set the first motor.

        If *torque* is ``None``,

        :return: Torque of the first motor.
        :rtype: float
        """
        if torque is not None:
            self._serial_write_q.put(
                self._command.set_property(
                    self.id,
                    self.ControlType.TORQUE.value,
                    (torque, self.second_torque(), 0),
                )
            )
        else:
            return self._get_property(self.PropertyType.FIRST_TORQUE)

    def second_torque(self, torque=None):
        """
        :param int degree: Torque to set the second motor.

        If *torque* is ``None``,

        :return: Torque of the second motor.
        :rtype: float
        """
        if torque is not None:
            self._serial_write_q.put(
                self._command.set_property(
                    self.id,
                    self.ControlType.TORQUE.value,
                    (self.first_torque(), torque, 0),
                )
            )
        else:
            return self._get_property(self.PropertyType.SECOND_TORQUE)

    def torque(self, first_torque=None, second_torque=None):
        """
        :param int first_torque: Torque to set the first motor.
        :param int second_torque: Torque to set the second motor.

        If *first_torque* is ``None`` and *second_torque* is ``None``,

        :return: Torque of the first motor , Torque of the second motor.
        :rtype: float
        """
        if first_torque is not None or second_torque is not None:
            first_torque = (
                self.first_torque() if first_torque is not None else first_torque
            )
            second_torque = (
                self.second_torque() if second_torque is None else second_torque
            )
            self._serial_write_q.put(
                self._command.set_property(
                    self.id,
                    self.ControlType.TORQUE.value,
                    (first_torque, second_torque, 0),
                )
            )
        return (
            self._get_property(self.PropertyType.FIRST_TORQUE),
            self._get_property(self.PropertyType.SECOND_TORQUE),
        )

    def speed(self, first_speed=None, second_speed=None):
        """
        :param int first_speed: Speed to set the first motor.
        :param int second_speed: Speed to set the second motor.

        If *first_speed* is ``None`` and *second_speed* is ``None``,

        :return: Speed of the first motor , Speed of the second motor.
        :rtype: float
        """
        if first_speed is not None or second_speed is not None:
            first_speed = self.first_speed() if first_speed is None else first_speed
            second_speed = self.second_speed() if second_speed is None else second_speed
            self._serial_write_q.put(
                self._command.set_property(
                    self.id,
                    self.ControlType.SPEED.value,
                    (first_speed, second_speed, 0),
                )
            )
        return (
            self._get_property(self.PropertyType.FIRST_SPEED),
            self._get_property(self.PropertyType.SECOND_SPEED),
        )

    def degree(self, first_degree=None, second_degree=None):
        """
        :param int first_degree: Degree to set the first motor.
        :param int second_degree: Degree to set the second motor.

        If *first_degree* is ``None`` and *second_degree* is ``None``,

        :return: Degree of the first motor , Degree of the second motor.
        :rtype: float
        """
        if first_degree is not None or second_degree is not None:
            first_degree = self.first_degree() if first_degree is None else first_degree
            second_degree = (
                self.second_degree() if second_degree is None else second_degree
            )
            self._serial_write_q.put(
                self._command.set_property(
                    self.id,
                    self.ControlType.DEGREE.value,
                    (first_degree, second_degree, 0),
                )
            )
        return (
            self._get_property(self.PropertyType.FIRST_DEGREE),
            self._get_property(self.PropertyType.SECOND_DEGREE),
        )
