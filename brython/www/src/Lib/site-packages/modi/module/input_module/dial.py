"""Dial module."""

from modi.module.input_module.input_module import InputModule


class Dial(InputModule):

    DEGREE = 2
    TURNSPEED = 3

    @property
    def degree(self) -> float:
        """Returns the angle of the dial between 0 and 100

        :return: The dial's angle.
        :rtype: float
        """
        return self._get_property(Dial.DEGREE)

    @property
    def turnspeed(self) -> float:
        """Returns the turn speed of the dial between 0 and 100

        :return: The dial's turn speed.
        :rtype: float
        """
        return self._get_property(Dial.TURNSPEED)
