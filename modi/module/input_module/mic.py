"""Mic module."""

from enum import IntEnum

from modi.module.input_module.input_module import InputModule


class Mic(InputModule):

    class PropertyType(IntEnum):
        VOLUME = 2
        FREQUENCY = 3

    def __init__(self, id_, uuid, msg_send_q):
        super().__init__(id_, uuid, msg_send_q)

    def get_volume(self) -> float:
        """Returns the volume of input sound between 0 and 100

        :return: Volume of input sound.
        :rtype: float
        """
        return self._get_property(self.PropertyType.VOLUME)

    def get_frequency(self) -> float:
        """Returns the frequency of input sound

        :return: Frequency of input sound.
        :rtype: float
        """
        return self._get_property(self.PropertyType.FREQUENCY)
