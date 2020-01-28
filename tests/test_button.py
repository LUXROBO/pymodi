#!/usr/bin/env python
# -*- coding: utf-8 -*-

import modi
import time
import mock
import unittest

from modi.module.button import Button


class TestButton(unittest.TestCase):
    """Tests for 'Button' class."""

    @mock.patch.object(Button, "get_clicked", return_value=True)
    def test_get_clicked(self, button):
        """Test get_clicked method."""
        ret_val = button.get_clicked()
        self.assertTrue(ret_val)

    @mock.patch.object(Button, "get_double_clicked", return_value=True)
    def test_get_double_clicked(self, button):
        """Test get_double_clicked method."""
        ret_val = button.get_double_clicked()
        self.assertTrue(ret_val)

    @mock.patch.object(Button, "get_pressed", return_value=True)
    def test_get_pressed(self, button):
        """Test get_pressed method."""
        ret_val = button.get_pressed()
        self.assertTrue(ret_val)

    @mock.patch.object(Button, "get_toggled", return_value=True)
    def test_get_toggled(self, button):
        """Test get_toggled method."""
        ret_val = button.get_toggled()
        self.assertTrue(ret_val)


if __name__ == "__main__":
    unittest.main()
