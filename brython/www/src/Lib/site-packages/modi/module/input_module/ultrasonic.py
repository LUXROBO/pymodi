"""Ultrasonic module."""

from modi.module.input_module.input_module import InputModule


class Ultrasonic(InputModule):

    DISTANCE = 2

    @property
    def distance(self) -> float:
        """Returns the distance of te object between 0 and 100

        :return: Distance to object.
        :rtype: float
        """
        return self._get_property(Ultrasonic.DISTANCE)
