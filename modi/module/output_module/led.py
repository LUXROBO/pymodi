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
        relative_color = self.red, self.green, self.blue
        absolute_color = tuple(map(lambda rc: rc * 255 // 100, relative_color))
        return absolute_color

    @rgb.setter
    @OutputModule._validate_property(nb_values=3, value_range=(0, 255))
    def rgb(self, color: Tuple[int, int, int]) -> None:
        """Sets the color of the LED light with given RGB values, and returns
        the current RGB values.

        :param color: RGB value to set
        :type color: Tuple[int, int, int]
        :return: None
        """
        if color == self.rgb:
            return
        relative_color = tuple(map(lambda c: c * 100 // 255, color))
        self._set_property(
            self._id,
            Led.SET_RGB,
            relative_color,
        )
        self.update_property(Led.RED, relative_color[0])
        self.update_property(Led.GREEN, relative_color[1])
        self.update_property(Led.BLUE, relative_color[2])

    def turn_on(self) -> None:
        """Turn on led at maximum brightness.

        :return: RGB value of the LED set to maximum brightness
        :rtype: None
        """
        self.rgb = 255, 255, 255

    def turn_off(self) -> None:
        """Turn off led.

        :return: None
        """
        self.rgb = 0, 0, 0

    @property
    def red(self) -> float:
        """Returns the current value of the red component of the LED

        :return: Red component
        :rtype: float
        """
        return self._get_property(Led.RED) * 255 // 100

    @red.setter
    @OutputModule._validate_property(nb_values=1, value_range=(0, 255))
    def red(self, red: int) -> None:
        """Sets the red component of the LED light by given value

        :param red: Red component to set
        :type red: int
        :return: None
        """
        self.rgb = red, 0, 0

    @property
    def green(self) -> float:
        """Returns the current value of the green component of the LED

        :return: Green component
        :rtype: float
        """
        return self._get_property(Led.GREEN) * 255 // 100

    @green.setter
    @OutputModule._validate_property(nb_values=1, value_range=(0, 255))
    def green(self, green: int) -> None:
        """Sets the green component of the LED light by given value

        :param green: Green component to set
        :type green: int
        :return: None
        """
        self.rgb = 0, green, 0

    @property
    def blue(self) -> float:
        """Returns the current value of the blue component of the LED

        :return: Blue component
        :rtype: float
        """
        return self._get_property(Led.BLUE) * 255 // 100

    @blue.setter
    @OutputModule._validate_property(nb_values=1, value_range=(0, 255))
    def blue(self, blue: int) -> None:
        """Sets the blue component of the LED light by given value

        :param blue: Blue component to set
        :type blue: int
        :return: None
        """
        self.rgb = 0, 0, blue
