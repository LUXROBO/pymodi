import modi

"""
Example script for the usage of gyro module
Make sure you connect 1 gyro module to your network module
"""

if __name__ == "__main__":
    bundle = modi.MODI()
    gyro = bundle.gyros[0]

    while True:
        print("Pitch: {0:<10}"
              "Roll: {1:<10}"
              "Yaw: {2:<10}".format(gyro.pitch, gyro.roll,
                                    gyro.yaw), end='\r')
