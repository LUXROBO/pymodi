#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `modi` package."""

import modi
import time
import base64
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


if __name__ == "__main__":
    unittest.main()
