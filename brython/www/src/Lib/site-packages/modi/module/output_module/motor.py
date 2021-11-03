"""Motor module."""

from typing import Tuple
from modi.module.output_module.output_module import OutputModule


class Motor(OutputModule):

    FIRST_TORQUE = 2
    SECOND_TORQUE = 10
    FIRST_SPEED = 3
    SECOND_SPEED = 11
    FIRST_DEGREE = 4
    SECOND_DEGREE = 12

    TORQUE = 16
    SPEED = 17
    DEGREE = 18
    CHANNEL = 19

    def __set_motor_channel(self,
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
            Motor.CHANNEL,
            (
                motor_channel,
                control_mode,
                control_value
            ),
        )

    @property
    def first_degree(self) -> float:
        """Returns first degree

        :return: first degree value
        :rtype: float
        """
        return self._get_property(Motor.FIRST_DEGREE)

    @first_degree.setter
    @OutputModule._validate_property(nb_values=1, value_range=(0, 100))
    def first_degree(self, degree_value: int) -> None:
        """Sets the angle of the motor at channel I

        :param degree_value: Angle to set the first motor.
        :type degree_value: int
        :return: None
        """
        _ = self.first_degree
        self.__set_motor_channel(0, 2, degree_value)
        self.update_property(Motor.FIRST_DEGREE, degree_value)

    @property
    def second_degree(self) -> float:
        """Returns second degree

        :return: second degree value
        :rtype: float
        """
        return self._get_property(Motor.SECOND_DEGREE)

    @second_degree.setter
    @OutputModule._validate_property(nb_values=1, value_range=(0, 100))
    def second_degree(self, degree_value: int) -> None:
        """Sets the angle of the motor at channel II

        :param degree_value: Angle to set the second motor.
        :type degree_value
        :return: None
        """
        _ = self.second_degree
        self.__set_motor_channel(1, 2, degree_value)
        self.update_property(Motor.SECOND_DEGREE, degree_value)

    @property
    def first_speed(self) -> float:
        """Returns first speed

        :return: first speed value
        :rtype: float
        """
        return self._get_property(Motor.FIRST_SPEED)

    @first_speed.setter
    @OutputModule._validate_property(nb_values=1, value_range=(-100, 100))
    def first_speed(self, speed_value: int) -> None:
        """Set the speed of the motor at channel I

        :param speed_value: Angular speed to set the first motor.
        :return: None
        """
        _ = self.first_speed
        self.__set_motor_channel(0, 1, speed_value)
        self.update_property(Motor.FIRST_SPEED, speed_value)

    @property
    def second_speed(self) -> float:
        """Returns second speed

        :return: second speed value
        :rtype: float
        """
        return self._get_property(Motor.SECOND_SPEED)

    @second_speed.setter
    @OutputModule._validate_property(nb_values=1, value_range=(-100, 100))
    def second_speed(self, speed_value: int) -> None:
        """Set the speed of the motor at channel II

        :param speed_value: Angular speed to set the second motor.
        :return: None
        """
        _ = self.second_speed
        self.__set_motor_channel(1, 1, speed_value)
        self.update_property(Motor.SECOND_SPEED, speed_value)

    @property
    def speed(self):
        """Returns speed value of two motors

        :return: Tuple[float, float]
        """
        return (
            self._get_property(Motor.FIRST_SPEED),
            self._get_property(Motor.SECOND_SPEED),
        )

    @speed.setter
    @OutputModule._validate_property(2, (-100, 100))
    def speed(self, speed_value: Tuple[int, int]) -> None:
        """Set the speed of the motors at both channels

        :param speed_value: Speed to set the motor.
        :type speed_value: Tuple[int, int]
        :return: None
        """
        _ = self.speed
        self.__set_motor_channel(0, 1, speed_value[0])
        self.__set_motor_channel(1, 1, speed_value[1])
        self.update_property(Motor.FIRST_SPEED, speed_value[0])
        self.update_property(Motor.SECOND_SPEED, speed_value[1])

    @property
    def degree(self) -> Tuple[float, float]:
        """Returns current angle

        :return: Angle of two motors
        :rtype: float
        """
        return (
            self._get_property(Motor.FIRST_DEGREE),
            self._get_property(Motor.SECOND_DEGREE),
        )

    @degree.setter
    @OutputModule._validate_property(nb_values=2, value_range=(0, 100))
    def degree(self, degree_value: Tuple[int, int]) -> None:
        """Set the angle of the motors at both channels

        :param degree_value: Degree to set
        :type degree_value: Tuple[int, int]
        :return: None
        """
        _ = self.degree
        self.__set_motor_channel(0, 2, degree_value[0])
        self.__set_motor_channel(1, 2, degree_value[1])
        self.update_property(Motor.FIRST_DEGREE, degree_value[0])
        self.update_property(Motor.SECOND_DEGREE, degree_value[1])
