#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `modi` package."""

# must
import modi
import time
import unittest

# from modi import a


class TestModi(unittest.TestCase):
    """Tests for `modi` package."""

    def test_1(self):
        """Set up test fixtures, if any."""
        bundle = modi.MODI()
        dial = bundle.dials[0]
        for _ in range(100):

            print(dial.degree(), dial.turnspeed())
            time.sleep(0.1)
        bundle.exit()

    def test_2(self):
        """Tear down test fixtures, if any."""

    def test_something(self):
        """Test something."""


if __name__ == "__main__":
    unittest.main()
