"""Led module."""

from enum import IntEnum
from typing import Tuple
from modi.module.output_module.output_module import OutputModule


class Led(OutputModule):

    class PropertyType(IntEnum):
        RED = 2
        GREEN = 3
        BLUE = 4

    class CommandType(IntEnum):
        SET_RGB = 16

    def __init__(self, id_, uuid, msg_send_q):
        super().__init__(id_, uuid, msg_send_q)
        self._type = "led"

    @property
    def rgb(self) -> Tuple[float, float, float]:
        return self.red, self.green, self.blue

    @rgb.setter
    def rgb(self, color: Tuple[int, int, int]) -> Tuple[float, float, float]:
        """Sets the color of the LED light with given RGB values, and returns
        the current RGB values.

        :param red: Red component to set or ``None``.
        :type red: int, optional
        :param green: Green component to set or ``None``.
        :type green: int, optional
        :param blue: Blue component to set or ``None``.
        :type blue: int, optional
        :return: Tuple of red, green
        :rtype: Tuple[float, float, float]
        """
        if isinstance(color, int):
            raise ValueError("Requires three values for red, green, and blue")

        red, green, blue = color
        color = (
            red if red is not None else self.red,
            green if green is not None else self.green,
            blue if blue is not None else self.blue)

        red, green, blue = color

        if red > 255 or blue > 255 or green > 255 or red < 0 or blue < 0\
                or green < 0:
            raise ValueError("Color should be in range of 0 ~ 255")

        self._set_property(
            self._id,
            self.CommandType.SET_RGB,
            color,
        )
        self._update_properties([property_type
                                 for property_type in self.PropertyType],
                                color)
        return color

    def turn_on(self) -> Tuple[float, float, float]:
        """Turn on led at maximum brightness.

        :return: RGB value of the LED set to maximum brightness
        :rtype: Tuple[float, float, float]
        """
        self.rgb = 255, 255, 255
        return 255, 255, 255

    def turn_off(self) -> Tuple[float, float, float]:
        """Turn off led.

        :return: RGB value of the LED turned off
        :rtype: Tuple[float, float, float]
        """
        self.rgb = 0, 0, 0
        return 0, 0, 0

    @property
    def red(self) -> float:
        """Returns the current value of the red component of the LED

        :return: Red component
        :rtype: float
        """
        return self._get_property(self.PropertyType.RED)

    @red.setter
    def red(self, red: int = 255) -> None:
        """Sets the red component of the LED light by given value

        :param red: Red component to set or ``None``.
        :type red: int, optional
        :return: None
        """
        self.rgb = red, None, None

    @property
    def green(self) -> float:
        """Returns the current value of the green component of the LED

        :return: Green component
        :rtype: float
        """
        return self._get_property(self.PropertyType.GREEN)

    @green.setter
    def green(self, green: int = 255) -> None:
        """Sets the green component of the LED light by given value

        :param green: Green component to set
        :type green: int, optional
        :return: None
        """
        self.rgb = None, green, None

    @property
    def blue(self) -> float:
        """Returns the current value of the blue component of the LED

        :return: Blue component
        :rtype: float
        """
        return self._get_property(self.PropertyType.BLUE)

    @blue.setter
    def blue(self, blue: int = 255) -> None:
        """Sets the blue component of the LED light by given value

        :param blue: Blue component to set
        :type blue: int, optional
        :return: None
        """
        self.rgb = None, None, blue
