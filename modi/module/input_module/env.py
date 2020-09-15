"""Env module."""

from modi.module.input_module.input_module import InputModule


class Env(InputModule):

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
        return self._get_property(Env.TEMPERATURE)

    @property
    def humidity(self) -> float:
        """Returns the value of humidity between 0 and 100

        :return: Humidity.
        :rtype: float
        """
        return self._get_property(Env.HUMIDITY)

    @property
    def brightness(self) -> float:
        """Returns the value of brightness between 0 and 100

        :return: Brightness.
        :rtype: float
        """
        return self._get_property(Env.BRIGHTNESS)

    @property
    def red(self) -> float:
        """Returns the value of red component of light

        :return: Red component of light.
        :rtype: float
        """
        return self._get_property(Env.RED)

    @property
    def green(self) -> float:
        """Returns the value of green component of light

        :return: Green component of light.
        :rtype: float
        """
        return self._get_property(Env.GREEN)

    @property
    def blue(self) -> float:
        """Returns the value of blue component of light

        :return: Blue component of light.
        :rtype: float
        """
        return self._get_property(Env.BLUE)
