"""Ultrasonic module."""

from enum import IntEnum

from modi.module.input_module.input_module import InputModule


class Ultrasonic(InputModule):

    class PropertyType(IntEnum):
        DISTANCE = 2

    def __init__(self, id_, uuid, msg_send_q):
        super().__init__(id_, uuid, msg_send_q)
        self._type = "ultrasonic"

    def get_distance(self) -> float:
        """Returns the distance of te object between 0 and 100

        :return: Distance to object.
        :rtype: float
        """
        return self._get_property(self.PropertyType.DISTANCE)
