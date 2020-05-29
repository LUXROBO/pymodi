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

    def __init__(self, id_, uuid, msg_send_q):
        super().__init__(id_, uuid, msg_send_q)

    def get_temperature(self) -> float:
        """Returns the value of temperature between 0 and 100

        :return: Temperature.
        :rtype: float
        """
        return self._get_property(self.PropertyType.TEMPERATURE)

    def get_humidity(self) -> float:
        """Returns the value of humidity between 0 and 100

        :return: Humidity.
        :rtype: float
        """
        return self._get_property(self.PropertyType.HUMIDITY)

    def get_brightness(self) -> float:
        """Returns the value of brightness between 0 and 100

        :return: Brightness.
        :rtype: float
        """
        return self._get_property(self.PropertyType.BRIGHTNESS)

    def get_red(self) -> float:
        """Returns the value of red component of light

        :return: Red component of light.
        :rtype: float
        """
        return self._get_property(self.PropertyType.RED)

    def get_green(self) -> float:
        """Returns the value of green component of light

        :return: Green component of light.
        :rtype: float
        """
        return self._get_property(self.PropertyType.GREEN)

    def get_blue(self) -> float:
        """Returns the value of blue component of light

        :return: Blue component of light.
        :rtype: float
        """
        return self._get_property(self.PropertyType.BLUE)
