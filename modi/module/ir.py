# -*- coding: utf-8 -*-

"""IR module."""

from __future__ import absolute_import

from enum import Enum

from modi.module.module import InputModule

class PropertyType(Enum):
    DISTANCE = 2
    BRIGHTNESS = 3

class Ir(InputModule):
    """
    :param int id: The id of the module.
    :param int uuid: The uuid of the module.
    :param modi: The :class:`~modi.modi.MODI` instance.
    :type modi: :class:`~modi.modi.MODI`
    """
    property_types = PropertyType

    def __init__(self, id, uuid, modi):
        super(Ir, self).__init__(id, uuid, modi)
        self._type = "ir"

    def distance(self):
        """
        :return: Distance to object.
        :rtype: float
        """
        return self._properties[PropertyType.DISTANCE]

    def brightness(self):
        """
        :return: Brightness.
        :rtype: float
        """
        return self._properties[PropertyType.BRIGHTNESS]