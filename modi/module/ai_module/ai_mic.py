import wave
import numpy as np
import time

from modi.util.audiolib import read, write
from modi.util.conn_util import is_modi_pi, AIModuleNotFoundException
from io import BytesIO
from typing import Tuple

# Import alsaaudio if the module is on raspberry pi
if is_modi_pi():
    import alsaaudio as audio


class AIMic:

    def __init__(self):
        if not self.is_ai_mic_connected():
            raise AIModuleNotFoundException("Cannot find the MODI AI Mic")

        self.RATE = 16000
        self.PERIOD = self.RATE // 8
        self.__mixer = None
        # Open the device object in non-blocking capture mode
        self.__device = audio.PCM(
            audio.PCM_CAPTURE,
            audio.PCM_NONBLOCK,
        )
        self.__set_device_attribute(self.__device)

        cards = audio.cards()
        for idx, card in enumerate(cards):
            if 'wm8960' in card:
                self.__mixer = audio.Mixer(
                    audio.mixers(idx)[0],
                    cardindex=idx
                )

        if not self.__mixer:
            raise AIModuleNotFoundException("Cannot find the MODI AI Mic")

    @staticmethod
    def is_ai_mic_connected():
        connected_devices = audio.pcms(audio.PCM_CAPTURE)
        for device in connected_devices:
            if 'wm8960' in device:
                return True
        return False

    @staticmethod
    def write_audio(file_path, data, sampling_rate):
        write(file_path, sampling_rate, data)

    def record(self, duration: float) -> Tuple[np.ndarray, float]:
        """ Record sound data catched by MODI AI shield

        :param duration: Duration for reconrding (Seconds)
        :type duration: float
        :param destination: File path of the destination
        :type destination: str
        :return: ndarray
        """
        bytes_wav = bytes()
        buffer = BytesIO(bytes_wav)
        audio_file = wave.open(buffer, 'wb')
        self.__set_attribute(audio_file)

        samples_written = 0
        while samples_written < self.RATE * duration:
            # Read data from device
            l, data = self.__device.read()

            if l:
                samples_written += l
                audio_file.writeframes(data)
                time.sleep(.001)
        audio_file.close()
        buffer.seek(0)
        return read(buffer)[::-1]

    def __set_attribute(self, audio_file):
        audio_file.setnchannels(2)
        audio_file.setsampwidth(2)
        audio_file.setframerate(self.RATE)

    def __set_device_attribute(self, device):
        device.setchannels(2)
        device.setrate(self.RATE)
        device.setformat(audio.PCM_FORMAT_S16_LE)
        self.PERIOD = device.setperiodsize(self.PERIOD)
