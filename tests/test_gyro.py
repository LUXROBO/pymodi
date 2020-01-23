#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `modi` package."""

# must
import modi
import time
import unittest
import timeit

# from modi import a


class TestModi(unittest.TestCase):
    """Tests for `modi` package."""

    def test_1(self):
        """Set up test fixtures, if any."""
        bundle = modi.MODI()
        gyro = bundle.gyros[0]
        now = time.time()
        past = now
        # for _ in range(100):
        while (now - past) < 10:
            now = time.time()
            print(
                gyro.get_roll(),
                gyro.get_pitch(),
                gyro.get_yaw(),
                gyro.get_angular_vel_x(),
                gyro.get_angular_vel_y(),
                gyro.get_angular_vel_z(),
                gyro.get_acceleration_x(),
                gyro.get_acceleration_y(),
                gyro.get_acceleration_z(),
                gyro.get_vibration(),
                bundle._json_recv_q.qsize(),
            )
            time.sleep(0.01)
        bundle.exit()

    def test_2(self):
        """Tear down test fixtures, if any."""

    def test_something(self):
        """Test something."""


if __name__ == "__main__":
    unittest.main()
