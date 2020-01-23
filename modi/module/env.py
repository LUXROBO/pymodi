# -*- coding: utf-8 -*-

"""Env module."""

from enum import Enum
from modi.module.module import InputModule


class Env(InputModule):
    """
    :param int id: The id of the module.
    :param int uuid: The uuid of the module.
    :param modi: The :class:`~modi.modi.MODI` instance.
    :type modi: :class:`~modi.modi.MODI`
    """

    class PropertyType(Enum):
        TEMPERATURE = 6
        HUMIDITY = 7
        BRIGHTNESS = 2
        RED = 3
        GREEN = 4
        BLUE = 5

    def __init__(self, module_id, module_uuid, modi, serial_write_q):
        super(Env, self).__init__(module_id, module_uuid, modi, serial_write_q)
        self._module_type = "env"

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
