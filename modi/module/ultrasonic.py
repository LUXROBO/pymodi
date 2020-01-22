# -*- coding: utf-8 -*-

"""Ultrasonic module."""

from __future__ import absolute_import

from enum import Enum

from modi.module.module import InputModule


class Ultrasonic(InputModule):
    """
    :param int id: The id of the module.
    :param int uuid: The uuid of the module.
    :param modi: The :class:`~modi.modi.MODI` instance.
    :type modi: :class:`~modi.modi.MODI`
    """

    class PropertyType(Enum):
        DISTANCE = 2

    def __init__(self, module_id, uuid, modi, serial_write_q):
        super(Ultrasonic, self).__init__(module_id, uuid, modi, serial_write_q)
        self._type = "ultrasonic"

    def distance(self):
        """
        :return: Distance to object.
        :rtype: float
        """
        return self._get_property(self.PropertyType.DISTANCE)
