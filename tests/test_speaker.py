#!/usr/bin/env python
# -*- coding: utf-8 -*-

import modi
import mock
import unittest

from modi.module.speaker import Speaker


class TestSpeaker(unittest.TestCase):
    """Tests for 'Speaker' class."""

    def setUp(self):
        """Set up test fixtures, if any."""
        self.mock_kwargs = {
            "module_id": -1,
            "module_uuid": -1,
            "modi": None,
            "serial_write_q": None,
        }
        self.speaker = Speaker(**self.mock_kwargs)

        def eval_set_property(x):
            pass

        self.speaker._set_property = mock.Mock(side_effect=eval_set_property)
        self.speaker._serial_write_q = mock.Mock()

    def tearDown(self):
        """Tear down test fixtures, if any."""
        del self.speaker

    def test_set_tune(self):
        """Test set_tune method."""
        pass

    def test_set_tune_with_none(self):
        """Test set_tune method with none input."""
        pass

    def test_set_frequency(self):
        """Test set_frequency method."""
        pass

    def test_set_frequency_with_none(self):
        """Test set_frequency method with none input."""
        pass

    def test_set_volume(self):
        """Test set_volume method."""
        pass

    def test_set_volume_with_none(self):
        """Test set_volume method with none input."""
        pass

    @mock.patch.object(Speaker, "set_tune")
    def test_set_off(self, mock_set_tune):
        """Test set_off method"""
        self.speaker.set_off()

        expeceted_values = frequency, volume = 0, 0
        mock_set_tune.assert_called_once_with(*expeceted_values)


if __name__ == "__main__":
    unittest.main()
