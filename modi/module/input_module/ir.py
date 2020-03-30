"""IR module."""

from enum import Enum

from modi.module.input_module.input_module import InputModule


class Ir(InputModule):

    class PropertyType(Enum):
        PROXIMITY = 2

    def __init__(self, id_, uuid, msg_send_q):
        super().__init__(id_, uuid, msg_send_q)

    def get_proximity(self):
        """
        :return: Distance to object.
        :rtype: float
        """
        return self._get_property(self.PropertyType.PROXIMITY)
