"""Mic module."""

from modi.module.input_module.input_module import InputModule


class Mic(InputModule):

    VOLUME = 2
    FREQUENCY = 3

    @property
    def volume(self) -> float:
        """Returns the volume of input sound between 0 and 100

        :return: Volume of input sound.
        :rtype: float
        """
        return self._get_property(Mic.VOLUME)

    @property
    def frequency(self) -> float:
        """Returns the frequency of input sound

        :return: Frequency of input sound.
        :rtype: float
        """
        return self._get_property(Mic.FREQUENCY)
