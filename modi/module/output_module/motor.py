"""Motor module."""

from enum import IntEnum
from typing import Tuple
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
        CHANNEL = 19

    def __init__(self, id_, uuid, msg_send_q):
        super().__init__(id_, uuid, msg_send_q)
        self._type = "motor"

    def set_motor_channel(self,
                          motor_channel: int, control_mode: int,
                          control_value: int = None) -> None:
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
        self._set_property(
            self._id,
            self.ControlType.CHANNEL,
            (
                motor_channel,
                control_mode,
                control_value,
                0x00 if control_value >= 0 else 0xFFFF,
            ),
        )

    @property
    def first_degree(self) -> float:
        """Returns first degree

        :return: first degree value
        :rtype: float
        """
        return self._get_property(self.PropertyType.FIRST_DEGREE)

    @first_degree.setter
    def first_degree(self, degree_value: int) -> None:
        """Sets the angle of the motor at channel I

        :param degree_value: Angle to set the first motor.
        :type degree_value: int
        :return: None
        """
        self.degree = degree_value, None

    @property
    def second_degree(self) -> float:
        """Returns second degree

        :return: second degree value
        :rtype: float
        """
        return self._get_property(self.PropertyType.SECOND_DEGREE)

    @second_degree.setter
    def second_degree(self, degree_value: int) -> None:
        """Sets the angle of the motor at channel II

        :param degree_value: Angle to set the second motor.
        :type degree_value
        :return: None
        """
        if degree_value < 0 or degree_value > 100:
            raise ValueError("Degree value should be in range of 0~100")
        self.degree = None, degree_value

    @property
    def first_speed(self) -> float:
        """Returns first speed

        :return: first speed value
        :rtype: float
        """
        return self._get_property(self.PropertyType.FIRST_SPEED)

    @first_speed.setter
    def first_speed(self, speed_value: int) -> None:
        """Set the speed of the motor at channel I

        :param speed_value: Angular speed to set the first motor.
        :return: None
        """
        self.speed = speed_value, None

    @property
    def second_speed(self) -> float:
        """Returns second speed

        :return: second speed value
        :rtype: float
        """
        return self._get_property(self.PropertyType.SECOND_SPEED)

    @second_speed.setter
    def second_speed(self, speed_value: int) -> None:
        """Set the speed of the motor at channel II

        :param speed_value: Angular speed to set the second motor.
        :return: Angular speed of the second motor.
        :rtype: float
        """
        self.speed = None, speed_value

    @property
    def first_torque(self) -> float:
        """Returns first torque

        :return: first torque value
        :rtype: float
        """
        return self._get_property(self.PropertyType.FIRST_TORQUE)

    @first_torque.setter
    def first_torque(self, torque_value: int) -> None:
        """Set the torque of the motor at channel I

        :param torque_value: Torque to set the first motor.
        :type torque_value: int
        :return: Torque of the first motor.
        :rtype: float
        """
        self.torque = torque_value, None

    @property
    def second_torque(self) -> float:
        """Returns second torque

        :return: second torque value
        :rtype: float
        """
        return self._get_property(self.PropertyType.SECOND_TORQUE)

    @second_torque.setter
    def second_torque(self, torque_value: int) -> None:
        """Set the torque of the motor at channel II

        :param torque_value: Torque to set the second motor.
        :type torque_value: int
        :return: None
        """
        self.torque = None, torque_value

    @property
    def torque(self) -> Tuple[float, float]:
        """Returns torque values of two motors

        :return: Torque
        :rtype: Tuple[float, float]
        """
        return (
            self._get_property(self.PropertyType.FIRST_TORQUE),
            self._get_property(self.PropertyType.SECOND_TORQUE),
        )

    @torque.setter
    def torque(self, torque_value: Tuple[int, int]) -> None:
        """Set the torque of the motors at both channels

        :param torque_value: Torque to set motor
        :type torque_value: Tuple[int, int]
        :return: None
        """
        if isinstance(torque_value, int):
            raise ValueError("Requires two values for each channel")
        if torque_value[0] is not None:
            if torque_value[0] < 0 or torque_value[0] > 100:
                raise ValueError("Torque value should be in range 0~100")
            self.set_motor_channel(0, 0, torque_value[0])
        if torque_value[1] is not None:
            if torque_value[1] < 0 or torque_value[1] > 100:
                raise ValueError("Torque value should be in range 0~100")
            self.set_motor_channel(1, 0, torque_value[1])

        self._update_properties(
            [self.PropertyType.FIRST_TORQUE, self.PropertyType.SECOND_TORQUE],
            torque_value)

    @property
    def speed(self):
        """Returns speed value of two motors

        :return: Tuple[float, float]
        """
        return (
            self._get_property(self.PropertyType.FIRST_SPEED),
            self._get_property(self.PropertyType.SECOND_SPEED),
        )

    @speed.setter
    def speed(self, speed_value: Tuple[int, int]) -> None:
        """Set the speed of the motors at both channels

        :param speed_value: Speed to set the motor.
        :type speed_value: Tuple[int, int]
        :return: None
        """
        if isinstance(speed_value, int):
            raise ValueError("Requires two values for each channel")
        if speed_value[0] is not None:
            if speed_value[0] < 0 or speed_value[0] > 100:
                raise ValueError("Speed value should be in range 0~100")
            self.set_motor_channel(0, 1, speed_value[0])
        if speed_value[1] is not None:
            if speed_value[1] < 0 or speed_value[1] > 100:
                raise ValueError("Speed value should be in range 0~100")
            self.set_motor_channel(1, 1, speed_value[1])

        self._update_properties(
            [self.PropertyType.FIRST_SPEED, self.PropertyType.SECOND_SPEED],
            speed_value)

    @property
    def degree(self) -> Tuple[float, float]:
        """Returns current angle

        :return: Angle of two motors
        :rtype: float
        """
        return (
            self._get_property(self.PropertyType.FIRST_DEGREE),
            self._get_property(self.PropertyType.SECOND_DEGREE),
        )

    @degree.setter
    def degree(self, degree_value: Tuple[int, int]) -> None:
        """Set the angle of the motors at both channels

        :param degree_value: Degree to set
        :type degree_value: Tuple[int, int]
        :return: Angle of the first motor , Angle of the second motor.
        :rtype: Tuple[float, float]
        """
        if isinstance(degree_value, int):
            raise ValueError("Requires two values for each channel")
        if degree_value[0] is not None:
            if degree_value[0] < 0 or degree_value[0] > 100:
                raise ValueError("Degree value should be in range 0~100")
            self.set_motor_channel(0, 2, degree_value[0])
        if degree_value[1] is not None:
            if degree_value[1] < 0 or degree_value[1] > 100:
                raise ValueError("Degree value should be in range 0~100")
            self.set_motor_channel(1, 2, degree_value[1])

        self._update_properties(
            [self.PropertyType.FIRST_DEGREE, self.PropertyType.SECOND_DEGREE],
            degree_value)
