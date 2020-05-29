"""Led module."""

from enum import IntEnum
from typing import Tuple, Optional
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

    def set_rgb(self, red: int = None, green: int = None,
                blue: int = None) -> Tuple[float, float, float]:
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
        if not (red is None and green is None and blue is None):
            message = self._set_property(
                self._id,
                self.CommandType.SET_RGB,
                (
                    red if red is not None else self.set_red(),
                    green if green is not None else self.set_green(),
                    blue if blue is not None else self.set_blue(),
                ),
            )
            self._msg_send_q.put(message)
        return self.set_red(), self.set_green(), self.set_blue()

    def set_on(self) -> Tuple[float, float, float]:
        """Turn on led at maximum brightness.

        :return: RGB value of the LED set to maximum brightness
        :rtype: Tuple[float, float, float]
        """
        return self.set_rgb(255, 255, 255)

    def set_off(self) -> Tuple[float, float, float]:
        """Turn off led.

        :return: RGB value of the LED turned off
        :rtype: Tuple[float, float, float]
        """
        return self.set_rgb(0, 0, 0)

    def set_red(self, red: int = None) -> float:
        """Sets the red component of the LED light by given value

        :param red: Red component to set or ``None``.
        :type red: int, optional
        :return: If *red* is ``None``. Red component.
        :rtype: float
        """
        if red is not None:
            self.set_rgb(red=red)
        return self._get_property(self.PropertyType.RED)

    def get_red(self) -> float:
        """Returns the current value of the red component of the LED

        :return: Red component
        :rtype: float
        """
        return self._get_property(self.PropertyType.RED)

    def set_green(self, green: int = None) -> float:
        """Sets the green component of the LED light by given value

        :param green: Green component to set or ``None``.
        :type green: int, optional
        :return: If *green* is ``None``. Green component.
        :rtype: float
        """
        if green is not None:
            self.set_rgb(green=green)
        return self._get_property(self.PropertyType.GREEN)

    def set_blue(self, blue: int = None) -> float:
        """Sets the blue component of the LED light by given value

        :param blue: Blue component to set or ``None``.
        :type blue: int, optional
        :return: If *blue* is ``None``. Blue component.
        :rtype: float
        """
        if blue is not None:
            self.set_rgb(blue=blue)
        return self._get_property(self.PropertyType.BLUE)
