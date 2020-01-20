#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `modi` package."""


# must
import modi
import unittest

# otherwise
import time
import multiprocessing


class TestModi(unittest.TestCase):
    """Tests for `modi` package."""

    def test_modi(self):
        print("start testing")
        print("number of cpus:", multiprocessing.cpu_count())
        """Test something."""
        bundle = modi.MODI()
        button = bundle.buttons[0]
        gyro = bundle.gyros[0]
        # motor = bundle.motors[0]

        # dial = bundle.dials[0]
        # env = bundle.envs[0]
        # ir = bundle.irs[0]
        # led = bundle.leds[0]
        # mic = bundle.mics[0]
        # display = bundle.displays[0
        # button.pressed()
        while True:
            time.sleep(0.01)
            print(button.pressed())
            # print('button.pressed():', button.pressed())
            # print(
            #    "aX aY aZ gX gY gZ",
            #    gyro.acceleration_x(),
            #    gyro.acceleration_y(),
            #    gyro.acceleration_z(),
            #    gyro.angular_vel_x(),
            #    gyro.angular_vel_y(),
            #    gyro.angular_vel_z(),
            #    button.pressed(),
            # )
            # print('aX', gyro.acceleration_x())
            # print('aY', gyro.acceleration_y())
            # print('aZ', gyro.acceleration_z())
            # print('gX', gyro.angular_vel_x())
            # print('gY', gyro.angular_vel_y())
            # print('gZ', gyro.angular_vel_z())
            # print(bundle._recv_q.qsize())
            pass


if __name__ == "__main__":
    unittest.main()

