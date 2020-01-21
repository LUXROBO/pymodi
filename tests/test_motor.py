#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `modi` package."""

import modi
import unittest
import time

from modi.module.motor import Motor


class TestMotor(unittest.TestCase):
    """Tests for `Motor` class."""

    def setUp(self):
        """Set up test fixtures, if any."""
        self.modi_inst = modi.MODI()
        self.motor = self.modi_inst.motors[0]

    def tearDown(self):
        """Tear down test fixtures, if any."""
        self.motor.speed(first_speed=0, second_speed=0)
        self.modi_inst.exit()
        time.sleep(1)

    def test_init(self):
        """Test initialization of motor module"""
        print("run test_init")
        self.assertIsInstance(self.motor, Motor)

    def test_torque(self):
        """Test torque method"""
        print("run test_torque")
        pass

    def test_speed(self):
        """Test speed method"""
        print("run test_speed")
        expected_speeds = (30, 30)
        self.motor.speed(*expected_speeds)
        time.sleep(2)
        actual_speeds = self.motor.speed()
        self.assertEqual(expected_speeds, actual_speeds)

    def test_degree(self):
        """Test degree method"""
        print("run test_degree")
        expected_degrees = (50, 50)
        self.motor.degree(*expected_degrees)
        time.sleep(2)
        actual_degrees = self.motor.degree()
        self.assertEqual(expected_degrees, actual_degrees)

    def test_individual_control(self):
        """Test individual motor control method"""
        pass


if __name__ == "__main__":
    unittest.main()
