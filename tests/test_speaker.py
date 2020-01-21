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
        time.sleep(1)

    def test_init(self):
        """Test initialization of speaker module"""
        self.assertIsInstance(self.speaker, Speaker)

    def test_basic_tune(self):
        """Test something."""
        self.speaker.tune(self.speaker.Scale.F_RA_6.value, 50)
        self.speaker.tune()
        time.sleep(3)
        self.assertEqual((self.speaker.Scale.F_RA_6.value, 50), self.speaker.tune())
        # for _ in range(30):
        #     print(self.speaker.tune())
        #     time.sleep(0.1)
        self.speaker.tune(0, 0)

    def test_custom_tune(self):
        """Test something."""

    def test_get_volume(self):
        """Test something."""

    def test_get_frequency(self):
        """Test something."""


if __name__ == "__main__":
    unittest.main()
