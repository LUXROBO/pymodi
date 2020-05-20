
import unittest

from unittest import mock

from modi.module.input_module.mic import Mic


class TestMic(unittest.TestCase):
    """Tests for 'Mic' class."""

    def setUp(self):
        """Set up test fixtures, if any."""
        mock_args = (-1, -1, None)
        self.mic = Mic(*mock_args)
        self.mic._get_property = mock.Mock()

    def tearDown(self):
        """Tear down test fixtures, if any."""
        del self.mic

    def test_get_volume(self):
        """Test get_volume method."""
        self.mic.get_volume()

        self.mic._get_property.assert_called_once_with(
            self.mic.PropertyType.VOLUME
        )

    def test_get_frequency(self):
        """Test get_frequency method."""
        self.mic.get_frequency()

        self.mic._get_property.assert_called_once_with(
            self.mic.PropertyType.FREQUENCY
        )
