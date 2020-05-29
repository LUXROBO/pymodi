"""Motor module."""

from enum import IntEnum
from typing import Optional, Tuple
from modi.module.output_module.output_module import OutputModule


class Motor(OutputModule):

    class PropertyType(IntEnum):
        FIRST_TORQUE = 2
        SECOND_TORQUE = 10
        FIRST_SPEED = 3
        SECOND_SPEED = 11
        FIRST_DEGREE = 4
        SECOND_DEGREE = 12

    class ControlType(IntEnum):
        TORQUE = 16
        SPEED = 17
        DEGREE = 18
        INV = 19

    def __init__(self, id_, uuid, msg_send_q):
        super().__init__(id_, uuid, msg_send_q)

    def set_motor_channel(self,
                          motor_channel: int, control_mode: int, control_value: int = None) -> Tuple[float, float]:
        """Select te motor channel for control
        Mode: 0:Torque 1:Speed 2:Angle (Torque is not implemented yet)

        :param motor_channel: channel number for control 0:Top 1:Bot
        :type motor_channel: int
        :param control_mode: Control mode of the motor to be selected
        :type control_mode: int
        :param control_value: value to control
        :type control_value: int, optional
        :return: current value of the motor control
        :rtype: Tuple[float, float]
        """
        if control_value is not None:
            self._msg_send_q.put(
                self._set_property(
                    self._id,
                    self.ControlType.INV,
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

    def set_first_degree(self, degree_value: int) -> int:
        """Sets the angle of the motor at channel I

        :param degree_value: Angle to set the first motor.
        :type degree_value: int, optional
        :return: If *degree* is ``None``, Angle of the first motor.
        :rtype: float, optional
        """
        self._msg_send_q.put(
            self._set_property(
                self._id,
                self.ControlType.DEGREE,
                (
                    degree_value,
                    self.get_second_degree(),
                    0,
                ),
            )
        )
        return degree_value

    def get_first_degree(self) -> float:
        """Returns first degree

        :return: first degree value
        :rtype: float
        """
        return self._get_property(self.PropertyType.FIRST_DEGREE)

    def set_second_degree(self, degree_value: int) -> float:
        """Sets the angle of the motor at channel II

        :param degree_value: Angle to set the second motor.
        :type degree_value
        :return: Angle of the second motor.
        :rtype: float
        """
        self._msg_send_q.put(
            self._set_property(
                self._id,
                self.ControlType.DEGREE,
                (self.get_first_degree(), degree_value, 0),
            )
        )
        return degree_value

    def get_second_degree(self) -> float:
        """Returns second degree

        :return: second degree value
        :rtype: float
        """
        return self._get_property(self.PropertyType.SECOND_DEGREE)

    def set_first_speed(self, speed_value: int = None) -> Optional[float]:
        """Set the speed of the motor at channel I

        :param speed_value: Angular speed to set the first motor.
        :return: If *speed* is ``None``, Angular speed of the first motor.
        :rtype: float
        """
        if speed_value is not None:
            self._msg_send_q.put(
                self._set_property(
                    self._id,
                    self.ControlType.SPEED,
                    (speed_value, self.set_first_speed(), 0),
                )
            )
        else:
            return self._get_property(self.PropertyType.FIRST_DEGREE)

    def set_second_speed(self, speed_value: int = None) -> Optional[float]:
        """Set the speed of the motor at channel II

        :param speed_value: Angular speed to set the second motor.
        :return: If *speed* is `None`, Angular speed of the second motor.
        :rtype: float
        """
        if speed_value is not None:
            self._msg_send_q.put(
                self._set_property(
                    self._id,
                    self.ControlType.SPEED,
                    (self.set_second_speed(), speed_value, 0),
                )
            )
        else:
            return self._get_property(self.PropertyType.SECOND_DEGREE)

    def set_first_torque(self, torque_value: int = None) -> Optional[float]:
        """Set the torque of the motor at channel I

        :param torque_value: Torque to set the first motor.
        :type torque_value: int
        :return: If *torque* is ``None``, Torque of the first motor.
        :rtype: float
        """
        if torque_value is not None:
            self._msg_send_q.put(
                self._set_property(
                    self._id,
                    self.ControlType.TORQUE,
                    (torque_value, self.set_second_torque(), 0),
                )
            )
        else:
            return self._get_property(self.PropertyType.FIRST_TORQUE)

    def set_second_torque(self, torque_value: int = None) -> Optional[float]:
        """Set the torque of the motor at channel II

        :param torque_value: Torque to set the second motor.
        :type torque_value: int
        :return: If *torque* is ``None``, Torque of the second motor.
        :rtype: float
        """
        if torque_value is not None:
            self._msg_send_q.put(
                self._set_property(
                    self._id,
                    self.ControlType.TORQUE,
                    (self.set_first_torque(), torque_value, 0),
                )
            )
        else:
            return self._get_property(self.PropertyType.SECOND_TORQUE)

    def set_torque(self, first_torque_value: int = None, second_torque_value: int = None) -> Tuple[float, float]:
        """Set the torque of the motors at both channels

        :param first_torque_value: Torque to set the first motor.
        :type first_torque_value: int, optional
        :param second_torque_value: Torque to set the second motor.
        :type second_torque_value: int, optional
        :return: If *first_torque* is ``None`` and *second_torque* is ``None``,
            Torque of the first motor , Torque of the second motor.
        :rtype: Tuple[float, float]
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
                self.ControlType.TORQUE,
                (first_torque_value, second_torque_value, 0),
            )
            self._msg_send_q.put(message)
        return (
            self._get_property(self.PropertyType.FIRST_TORQUE),
            self._get_property(self.PropertyType.SECOND_TORQUE),
        )

    def set_speed(self, first_speed_value: int = None, second_speed_value: int = None) -> Tuple[float, float]:
        """Set the speed of the motors at both channels

        :param first_speed_value: Speed to set the first motor.
        :type first_speed_value: int, optional
        :param second_speed_value: Speed to set the second motor.
        :type second_speed_value: int, optional
        :return: If *first_speed* is ``None`` and *second_speed* is ``None``,
            Speed of the first motor , Speed of the second motor.
        :rtype: Tuple[float, float]
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
                self.ControlType.SPEED,
                (first_speed_value, second_speed_value, 0),
            )
            self._msg_send_q.put(message)
        return (
            self._get_property(self.PropertyType.FIRST_SPEED),
            self._get_property(self.PropertyType.SECOND_SPEED),
        )

    def set_degree(self, first_degree_value: int,
                   second_degree_value: int) -> Tuple[float, float]:
        """Set the angle of the motors at both channels

        :param first_degree_value: Angle to set the first motor.
        :type first_degree_value: int, optional
        :param second_degree_value: Angle to set the second motor.
        :type second_degree_value: int, optional
        :return: Angle of the first motor , Angle of the second motor.
        :rtype: Tuple[float, float]
        """
        first_degree_value = (
            self.get_first_degree()
            if first_degree_value is None
            else first_degree_value
        )
        second_degree_value = (
            self.get_second_degree()
            if second_degree_value is None
            else second_degree_value
        )
        message = self._set_property(
            self._id,
            self.ControlType.DEGREE,
            (first_degree_value, second_degree_value, 0),
        )
        self._msg_send_q.put(message)
        return first_degree_value, second_degree_value

    def get_degree(self) -> float:
        """Returns current angle

        :return: Angle of two motors
        :rtype: float
        """
        return (
            self._get_property(self.PropertyType.FIRST_DEGREE),
            self._get_property(self.PropertyType.SECOND_DEGREE),
        )
