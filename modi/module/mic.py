# -*- coding: utf-8 -*-

"""Mic module."""

from __future__ import absolute_import

from enum import Enum

from modi.module.module import InputModule

class PropertyType(Enum):
    VOLUME = 2
    FREQUENCY = 3

class Mic(InputModule):
    """
    :param int id: The id of the module.
    :param int uuid: The uuid of the module.
    :param modi: The :class:`~modi.modi.MODI` instance.
    :type modi: :class:`~modi.modi.MODI`
    """
    property_types = PropertyType
    
    def __init__(self, id, uuid, modi):
        super(Mic, self).__init__(id, uuid, modi)
        self._type = "mic"

    def volume(self):
        """
        :return: Volume of input sound.
        :rtype: float
        """
        return self._properties[PropertyType.VOLUME]

    def frequency(self):
        """
        :return: Frequency of input sound.
        :rtype: float
        """
        return self._properties[PropertyType.FREQUENCY]
