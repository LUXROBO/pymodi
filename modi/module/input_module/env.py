"""Env module."""

from enum import Enum

from modi.module.input_module.input_module import InputModule


class Env(InputModule):

    class PropertyType(Enum):
        TEMPERATURE = 6
        HUMIDITY = 7
        BRIGHTNESS = 2
        RED = 3
        GREEN = 4
        BLUE = 5

    def __init__(self, id_, uuid, msg_send_q):
        super().__init__(id_, uuid, msg_send_q)

    def get_temperature(self) -> float:
        """
        :return: Temperature.
        :rtype: float
        """
        return self._get_property(self.PropertyType.TEMPERATURE)

    def get_humidity(self) -> float:
        """
        :return: Humidity.
        :rtype: float
        """
        return self._get_property(self.PropertyType.HUMIDITY)

    def get_brightness(self) -> float:
        """
        :return: Brightness.
        :rtype: float
        """
        return self._get_property(self.PropertyType.BRIGHTNESS)

    def get_red(self) -> float:
        """
        :return: Red component of light.
        :rtype: float
        """
        return self._get_property(self.PropertyType.RED)

    def get_green(self) -> float:
        """
        :return: Green component of light.
        :rtype: float
        """
        return self._get_property(self.PropertyType.GREEN)

    def get_blue(self) -> float:
        """
        :return: Blue component of light.
        :rtype: float
        """
        return self._get_property(self.PropertyType.BLUE)
