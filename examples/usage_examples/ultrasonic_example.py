import modi

"""
Example script for the usage of ultrasonic module
Make sure you connect 1 ultrasonic module to your network module
"""

if __name__ == "__main__":
    bundle = modi.MODI()
    ultrasonic = bundle.ultrasonics[0]

    while True:
        print("Distance: {0:<10}".format(ultrasonic.distance), end='\r')
