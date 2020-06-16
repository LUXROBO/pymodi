import alsaaudio as audio
import wave
import numpy as np
# from io import BytesIO


class AI_mic:

    def __init__(self):
        self.mixer = None
        self.__audio_file = None

        #Open the device object in nonblocking capture mode
        self.__device = audio.PCM(
            audio.PCM_CAPTURE,
            audio.PCM_NONBLOCK,
            device='default'
        )

        cards = audio.cards()
        for idx, card in enumerate(cards):
            if 'wm8960' in card:
                self.mixer = audio.Mixer(
                    audio.mixers(idx)[0],
                    cardindex=idx
                )
        if not self.mixer:
            raise Exception("Cannot find the MODI AI Mic")

    def record(self, duration: float) -> np.ndarray:
        """ Record sound data catched by MODI AI shield

        :param duration: Duration for reconrding (Seconds)
        :data duration: float
        :return: ndarray
        """
        pass



if __name__ == '__main__':

    mic = AI_mic()

    print(mic.mixer)

