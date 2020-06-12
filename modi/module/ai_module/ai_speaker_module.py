import alsaaudio as audio
import wave
from io import BytesIO
from scipy.io.wavfile import write
import numpy as np


class AISpeaker:
    def __init__(self):
        self.__device = audio.PCM()
        self.__mixer = None
        cards = audio.cards()
        for idx, card in enumerate(cards):
            if 'wm8960' in card:
                self.__mixer = audio.Mixer(
                    audio.mixers(idx)[0],
                    cardindex=idx)
        if not self.__mixer:
            raise Exception("Cannot find the MODI Speaker")

    def play(self, data, rate=44100):
        if isinstance(data, str):
            audio_file = wave.open(data, 'rb')
        else:
            audio_file = self.__numpy_to_wave(data, rate)

        # Set attributes
        self.__device.setchannels(audio_file.getnchannels())
        self.__device.setrate(audio_file.getframerate())

        # 8bit is unsigned in wav files
        if audio_file.getsampwidth() == 1:
            self.__device.setformat(audio.PCM_FORMAT_U8)
        # Otherwise we assume signed data, little endian
        elif audio_file.getsampwidth() == 2:
            self.__device.setformat(audio.PCM_FORMAT_S16_LE)
        elif audio_file.getsampwidth() == 3:
            self.__device.setformat(audio.PCM_FORMAT_S24_LE)
        elif audio_file.getsampwidth() == 4:
            self.__device.setformat(audio.PCM_FORMAT_S32_LE)
        else:
            raise ValueError('Unsupported format')

        period_size = audio_file.getframerate() // 8

        self.__device.setperiodsize(period_size)

        stream = audio_file.readframes(period_size)
        while stream:
            # Read data from stdin
            self.__device.write(stream)
            stream = audio_file.readframes(period_size)

    def play_tune(self, frequency, duration, volume=1, rate=44100):
        sine_wave = volume * (np.sin(2 * np.pi * np.arange(rate * duration) *
                                     frequency / rate))
        self.play(sine_wave, rate)

    @property
    def volume(self):
        return self.__mixer.getvolume()

    def set_volume(self, vol):
        self.__mixer.setvolume(vol)

    def mute(self):
        self.__mixer.setmute(1)

    def unmute(self):
        self.__mixer.setmute(0)

    def __numpy_to_wave(self, data, rate):
        buffer = BytesIO()
        write(buffer, rate, self.__float_to_pcm(data))
        return wave.open(buffer, "rb")

    @staticmethod
    def __float_to_pcm(signal, dtype='int16'):
        i = np.iinfo(dtype)
        abs_max = 2 ** (i.bits - 1)
        offset = i.min + abs_max
        return (signal * abs_max + offset).clip(i.min, i.max).astype(dtype)
