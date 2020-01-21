#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `modi` package."""

import modi
import unittest
import time

from modi.module.motor import Motor


class TestMotor(unittest.TestCase):
    modi_inst = None
    motor = None

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
        self.assertIsInstance(self.motor, Motor)

    def test_torque(self):
        """Test torque method"""
        pass

    def test_speed(self):
        """Test speed method"""
        expected_speeds = (30, 30)
        self.motor.speed(*expected_speeds)
        time.sleep(3)
        actual_speeds = self.motor.speed()
        self.assertEqual(expected_speeds, actual_speeds)

    def test_degree(self):
        """Test degree method"""
        expected_degrees = (50, 50)
        self.motor.degree


if __name__ == "__main__":
    unittest.main()
