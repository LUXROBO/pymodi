"""Mic module."""

from enum import Enum

from modi.module.input_module.input_module import InputModule


class Mic(InputModule):

    class PropertyType(Enum):
        VOLUME = 2
        FREQUENCY = 3

    def __init__(self, id_, uuid, msg_send_q):
        super().__init__(id_, uuid, msg_send_q)

    def get_volume(self):
        """
        :return: Volume of input sound.
        :rtype: float
        """
        return self._get_property(self.PropertyType.VOLUME)

    def get_frequency(self):
        """
        :return: Frequency of input sound.
        :rtype: float
        """
        return self._get_property(self.PropertyType.FREQUENCY)
