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

    class Scale(IntEnum):
        F_DO_1 = 32
        F_RE_1 = 36
        F_MI_1 = 41
        F_PA_1 = 43
        F_SOL_1 = 48
        F_RA_1 = 55
        F_SI_1 = 61
        F_DO_S_1 = 34
        F_RE_S_1 = 39
        F_PA_S_1 = 46
        F_SOL_S_1 = 52
        F_RA_S_1 = 58
        F_DO_2 = 65
        F_RE_2 = 73
        F_MI_2 = 82
        F_PA_2 = 87
        F_SOL_2 = 97
        F_RA_2 = 110
        F_SI_2 = 123
        F_DO_S_2 = 69
        F_RE_S_2 = 77
        F_PA_S_2 = 92
        F_SOL_S_2 = 103
        F_RA_S_2 = 116
        F_DO_3 = 130
        F_RE_3 = 146
        F_MI_3 = 165
        F_PA_3 = 174
        F_SOL_3 = 196
        F_RA_3 = 220
        F_SI_3 = 247
        F_DO_S_3 = 138
        F_RE_S_3 = 155
        F_PA_S_3 = 185
        F_SOL_S_3 = 207
        F_RA_S_3 = 233
        F_DO_4 = 261
        F_RE_4 = 293
        F_MI_4 = 329
        F_PA_4 = 349
        F_SOL_4 = 392
        F_RA_4 = 440
        F_SI_4 = 493
        F_DO_S_4 = 277
        F_RE_S_4 = 311
        F_PA_S_4 = 369
        F_SOL_S_4 = 415
        F_RA_S_4 = 466
        F_DO_5 = 523
        F_RE_5 = 587
        F_MI_5 = 659
        F_PA_5 = 698
        F_SOL_5 = 783
        F_RA_5 = 880
        F_SI_5 = 988
        F_DO_S_5 = 554
        F_RE_S_5 = 622
        F_PA_S_5 = 739
        F_SOL_S_5 = 830
        F_RA_S_5 = 932
        F_DO_6 = 1046
        F_RE_6 = 1174
        F_MI_6 = 1318
        F_PA_6 = 1397
        F_SOL_6 = 1567
        F_RA_6 = 1760
        F_SI_6 = 1975
        F_DO_S_6 = 1108
        F_RE_S_6 = 1244
        F_PA_S_6 = 1479
        F_SOL_S_6 = 1661
        F_RA_S_6 = 1864
        F_DO_7 = 2093
        F_RE_7 = 2349
        F_MI_7 = 2637
        F_PA_7 = 2793
        F_SOL_7 = 3135
        F_RA_7 = 3520
        F_SI_7 = 3951
        F_DO_S_7 = 2217
        F_RE_S_7 = 2489
        F_PA_S_7 = 2959
        F_SOL_S_7 = 3322
        F_RA_S_7 = 3729

    def __init__(self, id_, uuid, msg_send_q):
        super().__init__(id_, uuid, msg_send_q)
        self._type = "speaker"

    @property
    def tune(self) -> Tuple[float, float]:
        return (
            self.frequency,
            self.volume
        )

    @tune.setter
    def tune(self, tune_value: Tuple[int, int]) -> None:
        """Set tune for the speaker

        :param tune_value: Value of frequency and volume
        :type tune_value: Tuple[int, int]
        :return: None
        """
        if isinstance(tune_value, int):
            raise ValueError("Requires two values for frequency and volume")

        frequency_value = (tune_value[0]
                           if tune_value[0] is not None
                           else self.frequency)
        volume_value = (tune_value[1]
                        if tune_value[1] is not None
                        else self.volume)

        tune_value = (frequency_value, volume_value)

        self._set_property(
            self._id,
            self.CommandType.SET_TUNE,
            (frequency_value, volume_value,),
            self.PropertyDataType.FLOAT,
        )
        self._update_properties([property_type
                                 for property_type in self.PropertyType],
                                tune_value)

    @property
    def frequency(self) -> float:
        return self._get_property(self.PropertyType.FREQUENCY)

    @frequency.setter
    def frequency(self, frequency_value: float) -> None:
        """Set the frequency for the speaker

        :param frequency_value: Frequency to set
        :type frequency_value: float, optional
        :return: None
        """
        self.tune = frequency_value, None

    @property
    def volume(self) -> float:
        return self._get_property(self.PropertyType.VOLUME)

    @volume.setter
    def volume(self, volume_value: float) -> None:
        """Set the volume for the speaker

        :param volume_value: Volume to set
        :type volume_value: float
        :return: None
        """
        self.tune = None, volume_value

    def turn_off(self) -> None:
        """Turn off the sound

        :return: None
        """
        self.tune = 0, 0
