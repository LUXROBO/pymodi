import soundfile as sf
import sounddevice as sd

from modi.util.conn_util import AIModuleFaultsException
from typing import Union
from numpy import ndarray


class AISpeaker:
    def __init__(self):
        try:
            sd.check_output_settings('wm8960')
        except ValueError:
            raise AIModuleFaultsException("AI Speaker not found!!")

    def play(self, data: Union[str, ndarray], rate: float = None) -> None:
        """ Play wave file by a given filename or numpy array

        :param data: File path of numpy array
        :type data: Union[str, np.ndarray]
        :param rate: Sampling rate if the data is numpy array
        :type rate: int
        :return: None
        """
        if isinstance(data, str) and not rate:
            data, rate = sf.read(data)

        if rate == 44100:
            sd.play(data)
        else:
            sd.play(data, rate)

        sd.wait()
