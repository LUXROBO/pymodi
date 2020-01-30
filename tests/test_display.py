#!/usr/bin/env python
# -*- coding: utf-8 -*-

import modi
import mock
import struct
import base64
import unittest

import multiprocessing
from modi.module.display import Display


class TestDisplay(unittest.TestCase):
    """Tests for 'Display' class."""

    def setUp(self):
        """Set up test fixtures, if any."""
        self.mock_kwargs = {
            "module_id": -1,
            "module_uuid": -1,
            "modi": None,
            "serial_write_q": None,
        }
        self.display = Display(**self.mock_kwargs)
        self.display._set_property = mock.MagicMock(
            side_effect=self.__get_property_type
        )
        self.display._serial_write_q = mock.Mock()

    def tearDown(self):
        """Tear down test fixtures, if any."""
        del self.display

    # def test_set_text(self):
    #    """Test set_text method."""
    #    mock_text_input = "abcdef"
    #    actual_return = self.display.set_text(text=mock_text_input)

    #    ## check if clear has been called once
    #    # with mock.patch.object(Display, "clear") as mock_clear:
    #    #    mock_clear.assert_called_once()
    #    expected_clear_params = (
    #        self.mock_kwargs["module_id"],
    #        self.display.PropertyType.CLEAR,
    #        bytes(2),
    #        Display.PropertyDataType.RAW,
    #    )

    #    # check if set_property has been called once with the specified arguments
    #    expected_text_params = (
    #        self.mock_kwargs["module_id"],
    #        self.display.PropertyType.TEXT,
    #        mock_text_input,
    #        Display.PropertyDataType.STRING,
    #    )
    #    # expected_return = self.display._set_property.assert_called_once_with(
    #    #    *expected_text_params
    #    # )
    #    # self.display._serial_write_q.put.assert_called_once_with(expected_return)
    #    self.assertEqual(self.display._set_property.call_count, 2)
    #    a, b = self.display._set_property.call_args_list
    #    self.display._set_property.assert_has_calls(a, b)

    #    # self.assertEqual(self.display._serial_write_q.call_count)
    #    # self.assertEqual(expected_return, actual_return)

    # def test_set_variable(self):
    #    """Test set_variable method."""
    #    # display var range: -99999 ~ +99999
    #    expected_number = "-812.23"
    #    pos_x, pos_y = 5, 5
    #    msg_str = self.display.set_variable(expected_number, pos_x, pos_y)
    #    time.sleep(1)
    #    msg_str_frag = msg_str.split('"b":"')[1].split('"')[0]
    #    msg_str_frag_decoded = base64.b64decode(msg_str_frag)
    #    actual_number = struct.unpack("f", msg_str_frag_decoded[:4])[0]
    #    self.assertEqual(float(expected_number), round(actual_number, 2))

    def test_clear(self):
        """Test clear method."""
        self.display.clear()

        # check if set_property has been called once with the specified arguments
        expected_clear_params = (
            self.mock_kwargs["module_id"],
            self.display.PropertyType.CLEAR,
            bytes(2),
            Display.PropertyDataType.RAW,
        )
        self.display._set_property.assert_called_once_with(*expected_clear_params)
        self.display._serial_write_q.put.assert_called_once_with(
            self.display.PropertyType.CLEAR
        )

    def __get_property_type(self, id, property_type, data, property_data_type):
        return property_type


if __name__ == "__main__":
    unittest.main()
