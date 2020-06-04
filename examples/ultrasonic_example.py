import modi
import time

"""
Example script for the usage of ultrasonic module
Make sure you connect 1 ultrasonic module to your network module
"""

if __name__ == "__main__":
    bundle = modi.MODI(1)
    ultrasonic = bundle.ultrasonics[0]

    while True:
        print("Distance: {0:<10}".format(ultrasonic.get_distance()), end='\r')





