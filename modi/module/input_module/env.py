"""Env module."""

from enum import IntEnum

from modi.module.input_module.input_module import InputModule


class Env(InputModule):

    class PropertyType(IntEnum):
        TEMPERATURE = 6
        HUMIDITY = 7
        BRIGHTNESS = 2
        RED = 3
        GREEN = 4
        BLUE = 5

    @property
    def temperature(self) -> float:
        """Returns the value of temperature between 0 and 100

        :return: Temperature.
        :rtype: float
        """
        return self._get_property(self.PropertyType.TEMPERATURE)

    @property
    def humidity(self) -> float:
        """Returns the value of humidity between 0 and 100

        :return: Humidity.
        :rtype: float
        """
        return self._get_property(self.PropertyType.HUMIDITY)

    @property
    def brightness(self) -> float:
        """Returns the value of brightness between 0 and 100

        :return: Brightness.
        :rtype: float
        """
        return self._get_property(self.PropertyType.BRIGHTNESS)

    @property
    def red(self) -> float:
        """Returns the value of red component of light

        :return: Red component of light.
        :rtype: float
        """
        return self._get_property(self.PropertyType.RED)

    @property
    def green(self) -> float:
        """Returns the value of green component of light

        :return: Green component of light.
        :rtype: float
        """
        return self._get_property(self.PropertyType.GREEN)

    @property
    def blue(self) -> float:
        """Returns the value of blue component of light

        :return: Blue component of light.
        :rtype: float
        """
        return self._get_property(self.PropertyType.BLUE)
