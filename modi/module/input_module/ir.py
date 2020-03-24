"""IR module."""

from enum import Enum

from modi.module.input_module.input_module import InputModule


class Ir(InputModule):
    """
    :param int id: The id of the module.
    :param int uuid: The uuid of the module.
    :param modi: The :class:`~modi.modi.MODI` instance.
    :type modi: :class:`~modi.modi.MODI  `
    :param serial_write_q: multiprocessing.queue of the serial writing
    """

    class PropertyType(Enum):
        DISTANCE = 2

    def __init__(self, id_, uuid, serial_write_q):
        super(Ir, self).__init__(id_, uuid, serial_write_q)

    def get_distance(self):
        """
        :return: Distance to object.
        :rtype: float
        """
        return self._get_property(self.PropertyType.DISTANCE)
