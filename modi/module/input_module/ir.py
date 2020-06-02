"""IR module."""

from enum import IntEnum

from modi.module.input_module.input_module import InputModule


class Ir(InputModule):

    class PropertyType(IntEnum):
        PROXIMITY = 2

    def __init__(self, id_, uuid, msg_send_q):
        super().__init__(id_, uuid, msg_send_q, self.PropertyType)

    def get_proximity(self) -> float:
        """Returns the proximity value between 0 and 100

        :return: Distance to object.
        :rtype: float
        """
        return self._get_property(self.PropertyType.PROXIMITY)
