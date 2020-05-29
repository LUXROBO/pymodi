import modi
import time

"""
Example script for the usage of gyro module
Make sure you connect 1 gyro module to your network module
"""

if __name__ == "__main__":
    bundle = modi.MODI(1)
    gyro = bundle.gyros[0]

    while True:
        print("Pitch: {0:<10}"
              "Roll: {1:<10}"
              "Yaw: {2:<10}".format(gyro.get_pitch(), gyro.get_roll(),
                                    gyro.get_yaw()), end='\r')





