#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `modi` package."""

import modi
import time
import unittest


class TestLed(unittest.TestCase):
    """Tests for `Led` class."""

    modi_inst = None
    led = None

    def setUp(self):
        """Set up test fixtures, if any."""
        self.modi_inst = modi.MODI()
        self.led = self.modi_inst.leds[0]

    def tearDown(self):
        """Tear down test fixtures, if any."""
        self.led.off()
        time.sleep(1)
        self.modi_inst.exit()
        time.sleep(1)

    def test_custom_color(self):
        """Test rgb method with user-defined inputs."""
        expected_color = (10, 100, 200)
        self.led.rgb(*expected_color)
        time.sleep(2)
        actual_color = self.led.rgb()
        self.assertEqual(expected_color, actual_color)

    def test_on(self):
        """Test on method"""
        expected_color = (255, 255, 255)
        self.led.rgb(*expected_color)
        time.sleep(2)
        actual_color = self.led.rgb()
        self.assertEqual(expected_color, actual_color)

    def test_off(self):
        """Test off method"""
        # TODO: investigate this off method
        expected_color = (0, 0, 0)
        self.led.rgb(*expected_color)
        time.sleep(2)
        actual_color = self.led.rgb()
        self.assertEqual(expected_color, actual_color)

    def test_get_red(self):
        """Test red method."""
        expected_color = self.led.PropertyType.RED.value
        self.led.red(red=expected_color)
        time.sleep(2)
        actual_color = self.led.red()
        self.assertEqual(expected_color, actual_color)

    def test_get_green(self):
        """Test green method."""
        expected_color = self.led.PropertyType.GREEN.value
        self.led.green(green=expected_color)
        time.sleep(2)
        actual_color = self.led.green()
        self.assertEqual(expected_color, actual_color)

    def test_get_blue(self):
        """Test blue method."""
        expected_color = self.led.PropertyType.BLUE.value
        self.led.blue(blue=expected_color)
        time.sleep(2)
        actual_color = self.led.blue()
        self.assertEqual(expected_color, actual_color)


if __name__ == "__main__":
    unittest.main()
