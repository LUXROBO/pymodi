# -*- coding: utf-8 -*-

"""Speaker module."""

from __future__ import absolute_import

from enum import Enum

from modi.module.module import OutputModule

from modi._cmd import set_property
from modi._cmd import PropertyDataType

class PropertyType(Enum):
    FREQUENCY = 3
    VOLUME = 2

class Scale(Enum):
    F_DO_1 = 32
    F_RE_1 = 36
    F_MI_1 = 41
    F_PA_1 = 43
    F_SOL_1 = 48
    F_RA_1 = 55
    F_SO_1 = 61
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
    F_SO_2 = 123
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
    F_SO_3 = 247
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
    F_SO_4 = 493
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
    F_SO_5 = 988
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
    F_SO_6 = 1975
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
    F_SO_7 = 3951
    F_DO_S_7 = 2217
    F_RE_S_7 = 2489
    F_PA_S_7 = 2959
    F_SOL_S_7 = 3322
    F_RA_S_7 = 3729

class Speaker(OutputModule):
    """
    :param int id: The id of the module.
    :param int uuid: The uuid of the module.
    :param modi: The :class:`~modi.modi.MODI` instance.
    :type modi: :class:`~modi.modi.MODI`
    """
    property_types = PropertyType
    
    def __init__(self, id, uuid, modi):
        super(Speaker, self).__init__(id, uuid, modi)
        self._type = "speaker"

    def tune(self, frequency=None, volume=None):
        """
        * If either *frequency* or *volume* is not ``None``,

        :param float frequency: Frequency to set or ``None``.
        :param float volume: Volume to set or ``None``.

        The ``None`` component retains its previous value.

        * If *frequency* and *volume* are ``None``,

        :return: Tuple of frequency and volume.
        :rtype: tuple
        """
        if frequency == None and volume == None:
            return (self.frequency(), self.volume())
        else:
            self._modi().write(set_property(self.id, 16, (
                frequency if frequency != None else self.frequency(),
                volume if volume != None else self.volume()
            ), PropertyDataType.FLOAT))

    def frequency(self, frequency=None):
        """
        :param float frequency: Frequency to set or ``None``.

        If *frequency* is ``None``.

        :return: Frequency.
        :rtype: float
        """
        if frequency == None:
            return self._properties[PropertyType.FREQUENCY]
        else:
            self.tune(frequency=frequency)

    def volume(self, volume=None):
        """
        :param float volume: Volume to set or ``None``.

        If *volume* is ``None``.

        :return: Volume.
        :rtype: float
        """
        if volume == None:
            return self._properties[PropertyType.VOLUME]
        else:
            self.tune(volume=volume)

    def off(self):
        """Turn off.
        """
        self.tune(0, 0)
