import modi
import time

"""
Example script for the usage of mic module
Make sure you connect 1 mic module to your network module
"""

if __name__ == "__main__":
    bundle = modi.MODI(1)
    mic = bundle.mics[0]

    while True:
        print("Volume: {0:<10} freq: {1:<10}".format(mic.get_volume(),
              mic.get_frequency()), end='\r')





