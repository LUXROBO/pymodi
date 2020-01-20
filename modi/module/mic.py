# -*- coding: utf-8 -*-

"""Mic module."""

from __future__ import absolute_import

from enum import Enum

from modi.module.module import InputModule


class Mic(InputModule):
    """
    :param int id: The id of the module.
    :param int uuid: The uuid of the module.
    :param modi: The :class:`~modi.modi.MODI` instance.
    :type modi: :class:`~modi.modi.MODI`
    """

    class PropertyType(Enum):
        VOLUME = 2
        FREQUENCY = 3

    def __init__(self, id, uuid, modi):
        super(Mic, self).__init__(id, uuid, modi)
        self._type = "mic"

    def volume(self):
        """
        :return: Volume of input sound.
        :rtype: float
        """
        return self._write_property(self.PropertyType.VOLUME)

    def frequency(self):
        """
        :return: Frequency of input sound.
        :rtype: float
        """
        return self._write_property(self.PropertyType.FREQUENCY)
