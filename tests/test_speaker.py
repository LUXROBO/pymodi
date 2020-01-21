#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `modi` package."""

# must
import modi
import unittest
import time

from modi.module.speaker import Speaker


class TestSpeaker(unittest.TestCase):
    modi_inst = None
    speaker = None

    def setUp(self):
        """Set up test fixtures, if any."""
        self.modi_inst = modi.MODI()
        self.speaker = self.modi_inst.speakers[0]

    def tearDown(self):
        """Tear down test fixtures, if any."""
        self.modi_inst.exit()
        self.speaker.tune(0, 0)
        time.sleep(1)

    def test_init(self):
        """Test initialization of speaker module"""
        self.assertIsInstance(self.speaker, Speaker)

    def test_basic_tune(self):
        """Test tune method with pre-defined inputs"""
        expected_values = (self.speaker.Scale.F_RA_6.value, 50)
        self.speaker.tune(*expected_values)
        # TODO: remove delaying function
        time.sleep(2)
        actual_values = self.speaker.tune()
        self.assertEqual(expected_values, actual_values)

    def test_custom_tune(self):
        """Test tune method with custom inputs"""
        expected_values = (2350, 50)
        self.speaker.tune(*expected_values)
        time.sleep(2)
        actual_values = self.speaker.tune()
        self.assertEqual(expected_values, actual_values)

    def test_get_frequency(self):
        """Test frequency method"""
        expected_frequncy = self.speaker.Scale.F_RA_6.value
        self.speaker.frequency(frequency=expected_frequncy)
        time.sleep(2)
        actual_frequency = self.speaker.frequency()
        self.assertEqual(expected_frequncy, actual_frequency)

    def test_get_volume(self):
        """Test volume method"""
        expected_volume = 70
        self.speaker.volume(expected_volume)
        time.sleep(2)
        actual_volume = self.speaker.volume()
        self.assertEqual(expected_volume, actual_volume)


if __name__ == "__main__":
    unittest.main()
