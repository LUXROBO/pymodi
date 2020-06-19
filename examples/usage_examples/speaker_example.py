import modi
import time

"""
Example script for the usage of speaker module
Make sure you connect 1 speaker module to your network module
"""

if __name__ == "__main__":
    bundle = modi.MODI(1)
    speak = bundle.speakers[0]

    speak.set_tune(800, 70)
    time.sleep(3)
    speak.set_frequency(700)
    time.sleep(3)
    speak.set_volume(100)
    time.sleep(3)
    speak.set_off()
    time.sleep(3)
