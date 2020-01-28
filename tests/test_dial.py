#!/usr/bin/env python
# -*- coding: utf-8 -*-

import modi
import time
import mock
import unittest

from modi.module.dial import Dial


class TestDial(unittest.TestCase):
    """Tests for 'Dial' class."""

    @mock.patch.object(Dial, "get_degree", return_value=True)
    def test_get_degree(self, dial):
        """Test get_clicked method."""
        ret_val = dial.get_degree()
        self.assertTrue(ret_val)

    @mock.patch.object(Dial, "get_turnspeed", return_value=True)
    def test_get_turnspeed(self, dial):
        """Test get_clicked method."""
        ret_val = dial.get_turnspeed()
        self.assertTrue(ret_val)


if __name__ == "__main__":
    unittest.main()
