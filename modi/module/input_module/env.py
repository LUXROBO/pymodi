"""Env module."""

from enum import Enum

from modi.module.input_module.input_module import InputModule


class Env(InputModule):
    """
    :param int id: The id of the module.
    :param int uuid: The uuid of the module.
    :param serial_write_q: multiprocessing.queue of the serial writing
    """

    class PropertyType(Enum):
        TEMPERATURE = 6
        HUMIDITY = 7
        BRIGHTNESS = 2
        RED = 3
        GREEN = 4
        BLUE = 5

    def __init__(self, id_, uuid, serial_write_q):
        super(Env, self).__init__(id_, uuid, serial_write_q)

    def get_temperature(self):
        """
        :return: Temperature.
        :rtype: float
        """
        return self._get_property(self.PropertyType.TEMPERATURE)

    def get_humidity(self):
        """
        :return: Humidity.
        :rtype: float
        """
        return self._get_property(self.PropertyType.HUMIDITY)

    def get_brightness(self):
        """
        :return: Brightness.
        :rtype: float
        """
        return self._get_property(self.PropertyType.BRIGHTNESS)

    def get_red(self):
        """
        :return: Red component of light.
        :rtype: float
        """
        return self._get_property(self.PropertyType.RED)

    def get_green(self):
        """
        :return: Green component of light.
        :rtype: float
        """
        return self._get_property(self.PropertyType.GREEN)

    def get_blue(self):
        """
        :return: Blue component of light.
        :rtype: float
        """
        return self._get_property(self.PropertyType.BLUE)
