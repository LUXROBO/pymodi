#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `modi` package."""

import modi
import time
import struct
import base64
import unittest


class TestDisplay(unittest.TestCase):
    """Tests for `Display` class."""

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
        # display text maxlen -> 27
        expected_text = "abcdefghijklmnopqrstuv"
        msg_strs = self.display.text(expected_text)
        actual_text = str()
        for msg_str in msg_strs:
            msg_str_frag = msg_str.split('"b":"')[1].split('"')[0]
            msg_str_frag_decoded = base64.b64decode(msg_str_frag)
            actual_text_frag = msg_str_frag_decoded.decode()
            actual_text += actual_text_frag
        self.assertEqual(expected_text, actual_text)

    def test_variable(self):
        """Test variable method"""
        # display var range: -99999 ~ +99999
        # TODO: display cannot represent decimal points when -10,000 < x < 10,000
        expected_number = "-812.23"
        pos_x, pos_y = 5, 5
        msg_str = self.display.variable(expected_number, pos_x, pos_y)
        msg_str_frag = msg_str.split('"b":"')[1].split('"')[0]
        msg_str_frag_decoded = base64.b64decode(msg_str_frag)
        actual_number = struct.unpack("f", msg_str_frag_decoded[:4])[0]
        self.assertEqual(float(expected_number), round(actual_number, 2))


if __name__ == "__main__":
    unittest.main()
