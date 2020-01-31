#!/usr/bin/env python
# -*- coding: utf-8 -*-

import mock
import unittest

from modi.modi import MODI


class TestModi(unittest.TestCase):
    """Tests for 'modi' class."""

    def setUp(self):
        """Set up test fixtures, if any."""
        self.modi = MODI()
        pass

    def tearDown(self):
        """Tear down test fixtures, if any."""
        pass


if __name__ == "__main__":
    unittest.main()
