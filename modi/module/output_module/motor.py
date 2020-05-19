"""Motor module."""

from enum import Enum

from modi.module.output_module.output_module import OutputModule


class Motor(OutputModule):

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

    def __init__(self, id_, uuid, msg_send_q):
        super().__init__(id_, uuid, msg_send_q)

    def set_motor_channel(self,
                          motor_channel, control_mode, control_value=None):
        """
        :param motor_channel: Select motor channel for control
        :param control_mode: Control mode of the motor to be selected
        :param control_value: value to control
        Channel: 0:Top 1:Bot
        Mode: 0:Torque 1:Speed 2:Angle (Torque is not implemented yet)
        """
        if control_value is not None:
            self._msg_send_q.put(
                self._set_property(
                    self._id,
                    self.ControlType.INV.value,
                    (
                        motor_channel,
                        control_mode,
                        control_value,
                        0x00 if control_value >= 0 else 0xFFFF,
                    ),
                )
            )
        # TODO: implement return statement below
        # return (
        #    self._get_property(self.PropertyType.?),
        #    self._get_property(self.PropertyType.?),
        # )

    def set_first_degree(self, degree_value=None):
        """
        :param int degree: Angle to set the first motor.
        If *degree* is ``None``,
        :return: Angle of the first motor.
        :rtype: float
        """
        if degree_value is not None:
            self._msg_send_q.put(
                self._set_property(
                    self._id,
                    self.ControlType.DEGREE.value,
                    (
                        degree_value,
                        self._get_property(self.PropertyType.FIRST_DEGREE),
                        0,
                    ),
                )
            )
        else:
            return self._get_property(self.PropertyType.FIRST_DEGREE)

    def set_second_degree(self, degree_value=None):
        """
        :param int degree: Angle to set the second motor.
        If *degree* is ``None``,
        :return: Angle of the second motor.
        :rtype: float
        """
        if degree_value is not None:
            self._msg_send_q.put(
                self._set_property(
                    self._id,
                    self.ControlType.DEGREE.value,
                    (self.set_second_degree(), degree_value, 0),
                )
            )
        else:
            return self._get_property(self.PropertyType.SECOND_DEGREE)

    def set_first_speed(self, speed_value=None):
        """
        :param int degree: Angular speed to set the first motor.
        If *speed* is ``None``,
        :return: Angular speed of the first motor.
        :rtype: float
        """
        if speed_value is not None:
            self._msg_send_q.put(
                self._set_property(
                    self._id,
                    self.ControlType.SPEED.value,
                    (speed_value, self.set_first_speed(), 0),
                )
            )
        else:
            return self._get_property(self.PropertyType.FIRST_DEGREE)

    def set_second_speed(self, speed_value=None):
        """
        :param int degree: Angular speed to set the second motor.
        If *speed* is ``None``,
        :return: Angular speed of the second motor.
        :rtype: float
        """
        if speed_value is not None:
            self._msg_send_q.put(
                self._set_property(
                    self._id,
                    self.ControlType.SPEED.value,
                    (self.set_second_speed(), speed_value, 0),
                )
            )
        else:
            return self._get_property(self.PropertyType.SECOND_DEGREE)

    def set_first_torque(self, torque_value=None):
        """
        :param int degree: Torque to set the first motor.
        If *torque* is ``None``,
        :return: Torque of the first motor.
        :rtype: float
        """
        if torque_value is not None:
            self._msg_send_q.put(
                self._set_property(
                    self._id,
                    self.ControlType.TORQUE.value,
                    (torque_value, self.set_second_torque(), 0),
                )
            )
        else:
            return self._get_property(self.PropertyType.FIRST_TORQUE)

    def set_second_torque(self, torque_value=None):
        """
        :param int degree: Torque to set the second motor.
        If *torque* is ``None``,
        :return: Torque of the second motor.
        :rtype: float
        """
        if torque_value is not None:
            self._msg_send_q.put(
                self._set_property(
                    self._id,
                    self.ControlType.TORQUE.value,
                    (self.set_first_torque(), torque_value, 0),
                )
            )
        else:
            return self._get_property(self.PropertyType.SECOND_TORQUE)

    def set_torque(self, first_torque_value=None, second_torque_value=None):
        """
        :param int first_torque: Torque to set the first motor.
        :param int second_torque: Torque to set the second motor.
        If *first_torque* is ``None`` and *second_torque* is ``None``,
        :return: Torque of the first motor , Torque of the second motor.
        :rtype: float
        """
        if first_torque_value is not None or second_torque_value is not None:
            first_torque_value = (
                self.set_first_torque()
                if first_torque_value is None
                else first_torque_value
            )
            second_torque_value = (
                self.set_second_torque()
                if second_torque_value is None
                else second_torque_value
            )
            message = self._set_property(
                self._id,
                self.ControlType.TORQUE.value,
                (first_torque_value, second_torque_value, 0),
            )
            self._msg_send_q.put(message)
        return (
            self._get_property(self.PropertyType.FIRST_TORQUE),
            self._get_property(self.PropertyType.SECOND_TORQUE),
        )

    def set_speed(self, first_speed_value=None, second_speed_value=None):
        """
        :param int first_speed: Speed to set the first motor.
        :param int second_speed: Speed to set the second motor.
        If *first_speed* is ``None`` and *second_speed* is ``None``,
        :return: Speed of the first motor , Speed of the second motor.
        :rtype: float
        """
        if first_speed_value is not None or second_speed_value is not None:
            first_speed_value = (
                self.set_first_speed()
                if first_speed_value is None
                else first_speed_value
            )
            second_speed_value = (
                self.set_second_speed()
                if second_speed_value is None
                else second_speed_value
            )
            message = self._set_property(
                self._id,
                self.ControlType.SPEED.value,
                (first_speed_value, second_speed_value, 0),
            )
            self._msg_send_q.put(message)
        return (
            self._get_property(self.PropertyType.FIRST_SPEED),
            self._get_property(self.PropertyType.SECOND_SPEED),
        )

    def set_degree(self, first_degree_value=None, second_degree_value=None):
        """
        :param int first_degree: Degree to set the first motor.
        :param int second_degree: Degree to set the second motor.
        If *first_degree* is ``None`` and *second_degree* is ``None``,
        :return: Degree of the first motor , Degree of the second motor.
        :rtype: float
        """
        if first_degree_value is not None or second_degree_value is not None:
            first_degree_value = (
                self.set_first_degree()
                if first_degree_value is None
                else first_degree_value
            )
            second_degree_value = (
                self.set_second_degree()
                if second_degree_value is None
                else second_degree_value
            )
            message = self._set_property(
                self._id,
                self.ControlType.DEGREE.value,
                (first_degree_value, second_degree_value, 0),
            )
            self._msg_send_q.put(message)
        return (
            self._get_property(self.PropertyType.FIRST_DEGREE),
            self._get_property(self.PropertyType.SECOND_DEGREE),
        )
