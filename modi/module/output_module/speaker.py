"""Speaker module."""

from typing import Tuple
from modi.module.output_module.output_module import OutputModule


class Speaker(OutputModule):

    FREQUENCY = 3
    VOLUME = 2

    SET_TUNE = 16

    SCALE_TABLE = {
        'FA5': 698,
        'SOL5': 783,
        'LA5': 880,
        'TI5': 988,
        'DO#5': 554,
        'RE#5': 622,
        'FA#5': 739,
        'SOL#5': 830,
        'LA#5': 932,
        'DO6': 1046,
        'RE6': 1174,
        'MI6': 1318,
        'FA6': 1397,
        'SOL6': 1567,
        'LA6': 1760,
        'TI6': 1975,
        'DO#6': 1108,
        'RE#6': 1244,
        'FA#6': 1479,
        'SOL#6': 1661,
        'LA#6': 1864,
        'DO7': 2093,
        'RE7': 2349,
        'MI7': 2637
    }

    def __init__(self, id_, uuid, conn_task):
        super().__init__(id_, uuid, conn_task)
        # Default frequency of MODI Speaker
        self.frequency = 1318

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

        if isinstance(tune_value[0], str):
            tune_value = (
                Speaker.SCALE_TABLE.get(tune_value[0], -1),
                tune_value[1]
            )

        if tune_value[0] < 0:
            raise ValueError("Not a supported frequency value")

        self._set_property(
            self._id,
            Speaker.SET_TUNE,
            tune_value,
            OutputModule.FLOAT,
        )
        self.update_property(Speaker.FREQUENCY, tune_value[0])
        self.update_property(Speaker.VOLUME, tune_value[1])

    @property
    def frequency(self) -> float:
        return self._get_property(Speaker.FREQUENCY)

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
        return self._get_property(Speaker.VOLUME)

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
