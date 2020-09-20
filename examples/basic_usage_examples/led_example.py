import modi
import time

"""
Example script for the usage of led module
Make sure you connect 1 led module to your network module
"""

if __name__ == "__main__":
    bundle = modi.MODI(1)
    led = bundle.leds[0]

    led.blue = 255
    time.sleep(3)
    led.blue = 0
    time.sleep(1)
    led.green = 255
    time.sleep(3)
    led.green = 0
    time.sleep(1)
    led.red = 255
    time.sleep(3)
    for c in range(255):
        led.rgb = 255-c, c, 0
        time.sleep(0.02)

    led.turn_on()
    time.sleep(2)
    led.turn_off()
    time.sleep(1)
