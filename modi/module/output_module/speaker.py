"""Speaker module."""

from enum import IntEnum
from typing import Tuple
from modi.module.output_module.output_module import OutputModule


class Speaker(OutputModule):
    class PropertyType(IntEnum):
        FREQUENCY = 3
        VOLUME = 2

    class CommandType(IntEnum):
        SET_TUNE = 16

    @property
    def tune(self) -> Tuple[float, float]:
        return (
            self.frequency,
            self.volume
        )

    @tune.setter
    @OutputModule._validate_property(nb_values=2)
    def tune(self, tune_value: Tuple[int, int]) -> None:
        """Set tune for the speaker

        :param tune_value: Value of frequency and volume
        :type tune_value: Tuple[int, int]
        :return: None
        """
        if tune_value == self.tune:
            return
        self._set_property(
            self._id,
            self.CommandType.SET_TUNE,
            tune_value,
            self.PropertyDataType.FLOAT,
        )
        self.update_property(self.PropertyType.FREQUENCY, tune_value[0])
        self.update_property(self.PropertyType.VOLUME, tune_value[1])

    @property
    def frequency(self) -> float:
        return self._get_property(self.PropertyType.FREQUENCY)

    @frequency.setter
    @OutputModule._validate_property(nb_values=1)
    def frequency(self, frequency_value: float) -> None:
        """Set the frequency for the speaker

        :param frequency_value: Frequency to set
        :type frequency_value: float, optional
        :return: None
        """
        self.tune = frequency_value, self.volume

    @property
    def volume(self) -> float:
        """Returns current volume

        :return: Volume value
        :rtype: float
        """
        return self._get_property(self.PropertyType.VOLUME)

    @volume.setter
    @OutputModule._validate_property(nb_values=1, value_range=(0, 100))
    def volume(self, volume_value: float) -> None:
        """Set the volume for the speaker

        :param volume_value: Volume to set
        :type volume_value: float
        :return: None
        """
        self.tune = self.frequency, volume_value

    def turn_off(self) -> None:
        """Turn off the sound

        :return: None
        """
        self.tune = 0, 0
