# -*- coding: utf-8 -*-

"""Dial module."""

from __future__ import absolute_import

from enum import Enum

from modi.module.module import InputModule

class PropertyType(Enum):
    DEGREE = 2 

class Dial(InputModule):
    """
    :param int id: The id of the module.
    :param int uuid: The uuid of the module.
    :param modi: The :class:`~modi.modi.MODI` instance.
    :type modi: :class:`~modi.modi.MODI`
    """
    property_types = PropertyType
    
    def __init__(self, id, uuid, modi):
        super(Dial, self).__init__(id, uuid, modi)
        self._type = "dial"

    def degree(self):
        """
        :return: The dial's angle.
        :rtype: float
        """
        return self._properties[PropertyType.DEGREE]