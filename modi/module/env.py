# -*- coding: utf-8 -*-

"""Env module."""

from __future__ import absolute_import

from enum import Enum
from modi.module.module import InputModule

class PropertyType(Enum):
    TEMPERATURE = 6
    HUMIDITY = 7
    BRIGHTNESS = 2
    RED = 3
    GREEN = 4
    BLUE = 5

class Env(InputModule):
    """
    :param int id: The id of the module.
    :param int uuid: The uuid of the module.
    :param modi: The :class:`~modi.modi.MODI` instance.
    :type modi: :class:`~modi.modi.MODI`
    """
    property_types = PropertyType
    
    def __init__(self, id, uuid, modi):
        super(Env, self).__init__(id, uuid, modi)
        self._type = "env"

    def temperature(self):
        """
        :return: Temperature.
        :rtype: float
        """
        return self._properties[PropertyType.TEMPERATURE]

    def humidity(self):
        """
        :return: Humidity.
        :rtype: float
        """
        return self._properties[PropertyType.HUMIDITY]

    def brightness(self):
        """
        :return: Brightness.
        :rtype: float
        """
        return self._properties[PropertyType.BRIGHTNESS]

    def red(self):
        """
        :return: Red component of light.
        :rtype: float
        """
        return self._properties[PropertyType.RED]

    def green(self):
        """
        :return: Green component of light.
        :rtype: float
        """
        return self._properties[PropertyType.GREEN]

    def blue(self):
        """
        :return: Blue component of light.
        :rtype: float
        """
        return self._properties[PropertyType.BLUE]