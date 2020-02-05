import unittest

from unittest import mock

from modi.module.input_module.ir import Ir


class TestIr(unittest.TestCase):
    """Tests for 'Ir' package."""

    def setUp(self):
        """Set up test fixtures, if any."""
        mock_args = (-1, -1, None)
        self.ir = Ir(*mock_args)
        self.ir._get_property = mock.MagicMock()

    def tearDown(self):
        """Tear down test fixtures, if any."""
        del self.ir

    def test_get_distance(self):
        """Test get_distance method."""
        self.ir.get_distance()
        self.ir._get_property.assert_called_once_with(
            self.ir.PropertyType.DISTANCE)

    def test_get_brightness(self):
        """Test get_brightness method."""
        self.ir.get_brightness()
        self.ir._get_property.assert_called_once_with(
            self.ir.PropertyType.BRIGHTNESS)


if __name__ == "__main__":
    unittest.main()
