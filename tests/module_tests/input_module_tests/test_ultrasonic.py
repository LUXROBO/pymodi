import unittest

from unittest import mock

from modi.module.input_module.ultrasonic import Ultrasonic


class TestUltrasonic(unittest.TestCase):
    """Tests for 'Ultrasonic' class."""

    def setUp(self):
        """Set up test fixtures, if any."""
        mock_args = (-1, -1, None)
        self.ultrasonic = Ultrasonic(*mock_args)
        self.ultrasonic._get_property = mock.Mock()

    def tearDown(self):
        """Tear down test fixtures, if any."""
        del self.ultrasonic

    def test_get_distance(self):
        """Test get_distance method."""
        self.ultrasonic.get_distance()

        self.ultrasonic._get_property.assert_called_once_with(
            self.ultrasonic.PropertyType.DISTANCE
        )
