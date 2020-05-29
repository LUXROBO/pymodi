import modi
import time

"""
Example script for the usage of led module
Make sure you connect 1 led module to your network module
"""

if __name__ == "__main__":
    bundle = modi.MODI(1)
    led = bundle.leds[0]

    led.set_blue(255)
    time.sleep(3)
    led.set_blue(0)
    time.sleep(1)
    led.set_green(255)
    time.sleep(3)
    led.set_green(0)
    time.sleep(1)
    led.set_red(255)
    time.sleep(3)
    for c in range(255):
        led.set_rgb(255-c, c, 0)
        time.sleep(0.02)

    led.set_on()
    time.sleep(2)
    led.set_off()
    time.sleep(1)

