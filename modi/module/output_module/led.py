"""Led module."""

from typing import Tuple
from modi.module.output_module.output_module import OutputModule


class Led(OutputModule):

    RED = 2
    GREEN = 3
    BLUE = 4

    SET_RGB = 16

    @property
    def rgb(self) -> Tuple[float, float, float]:
        return self.red, self.green, self.blue

    @rgb.setter
    @OutputModule._validate_property(nb_values=3, value_range=(0, 100))
    def rgb(self, color: Tuple[int, int, int]) -> None:
        """Sets the color of the LED light with given RGB values, and returns
        the current RGB values.

        :param color: RGB value to set
        :type color: Tuple[int, int, int]
        :return: None
        """
        if color == self.rgb:
            return
        self._set_property(
            self._id,
            Led.SET_RGB,
            color,
        )
        self.update_property(Led.RED, color[0])
        self.update_property(Led.GREEN, color[1])
        self.update_property(Led.BLUE, color[2])

    @property
    def red(self) -> float:
        """Returns the current value of the red component of the LED

        :return: Red component
        :rtype: float
        """
        return self._get_property(Led.RED)

    @red.setter
    @OutputModule._validate_property(nb_values=1, value_range=(0, 100))
    def red(self, red: int) -> None:
        """Sets the red component of the LED light by given value

        :param red: Red component to set
        :type red: int
        :return: None
        """
        self.rgb = red, self.green, self.blue

    @property
    def green(self) -> float:
        """Returns the current value of the green component of the LED

        :return: Green component
        :rtype: float
        """
        return self._get_property(Led.GREEN)

    @green.setter
    @OutputModule._validate_property(nb_values=1, value_range=(0, 100))
    def green(self, green: int) -> None:
        """Sets the green component of the LED light by given value

        :param green: Green component to set
        :type green: int
        :return: None
        """
        self.rgb = self.red, green, self.blue

    @property
    def blue(self) -> float:
        """Returns the current value of the blue component of the LED

        :return: Blue component
        :rtype: float
        """
        return self._get_property(Led.BLUE)

    @blue.setter
    @OutputModule._validate_property(nb_values=1, value_range=(0, 100))
    def blue(self, blue: int) -> None:
        """Sets the blue component of the LED light by given value

        :param blue: Blue component to set
        :type blue: int
        :return: None
        """
        self.rgb = self.red, self.green, blue

    #
    # Legacy Support
    #
    def turn_on(self) -> None:
        """Turn on led at maximum brightness.

        :return: RGB value of the LED set to maximum brightness
        :rtype: None
        """
        self.rgb = 100, 100, 100

    def turn_off(self) -> None:
        """Turn off led.

        :return: None
        """
        self.rgb = 0, 0, 0
