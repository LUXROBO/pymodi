#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `modi` package."""

import modi
import time
import unittest


class TestDisplay(unittest.TestCase):
    """Tests for `Display` class."""

    modi_inst = None
    display = None

    def setUp(self):
        """Set up test fixtures, if any."""
        self.modi_inst = modi.MODI()
        self.display = self.modi_inst.displays[0]

    def tearDown(self):
        """Tear down test fixtures, if any."""
        self.display.clear()
        self.modi_inst.exit()
        time.sleep(1)

    def test_text(self):
        """Test text method"""
        self.display.text("hello")
        time.sleep(3)


if __name__ == "__main__":
    unittest.main()
