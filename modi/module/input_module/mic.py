"""Mic module."""

from enum import Enum

from modi.module.input_module.input_module import InputModule


class Mic(InputModule):
    """
    :param int id: The id of the module.
    :param int uuid: The uuid of the module.
    :param serial_write_q: multiprocessing.queue of the serial writing
    """

    class PropertyType(Enum):
        VOLUME = 2
        FREQUENCY = 3

    def __init__(self, id_, uuid, serial_write_q):
        super(Mic, self).__init__(id_, uuid, serial_write_q)
        self._type = "mic"

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
