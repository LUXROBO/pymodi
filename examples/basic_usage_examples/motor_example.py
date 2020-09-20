import modi
import time

"""
Example script for the usage of motor module
Make sure you connect 1 motor module to your network module
"""

if __name__ == "__main__":
    bundle = modi.MODI(1)
    motor = bundle.motors[0]

    motor.degree = 0, 0
    time.sleep(3)
    motor.first_degree = 50
    time.sleep(3)
    motor.second_degree = 50
    time.sleep(3)
    motor.speed = 50, 50
    time.sleep(3)
    motor.first_speed = 100
    time.sleep(3)
    motor.second_speed = 100
    time.sleep(3)
    motor.speed = 0, 0
    time.sleep(1)
