import unittest

from unittest import mock

from modi.module.input_module.env import Env


class TestEnv(unittest.TestCase):
    """Tests for 'Env' class."""

    def setUp(self):
        """Set up test fixtures, if any."""
        mock_args = (-1, -1, None)
        self.env = Env(*mock_args)
        self.env._get_property = mock.Mock()

    def tearDown(self):
        """Tear down test fixtures, if any."""
        del self.env

    def test_get_temperature(self):
        """Test get_temperature method."""
        _ = self.env.temperature
        self.env._get_property.assert_called_once_with(
            self.env.PropertyType.TEMPERATURE
        )

    def test_get_humidity(self):
        """Test get_humidity method."""
        _ = self.env.humidity
        self.env._get_property.assert_called_once_with(
            self.env.PropertyType.HUMIDITY)

    def test_get_brightness(self):
        """Test get_brightness method."""
        _ = self.env.brightness
        self.env._get_property.assert_called_once_with(
            self.env.PropertyType.BRIGHTNESS)

    def test_get_red(self):
        """Test get_red method."""
        _ = self.env.red
        self.env._get_property.assert_called_once_with(
            self.env.PropertyType.RED)

    def test_get_green(self):
        """Test get_green method."""
        _ = self.env.green
        self.env._get_property.assert_called_once_with(
            self.env.PropertyType.GREEN)

    def test_get_blue(self):
        """Test get_blue method."""
        _ = self.env.blue
        self.env._get_property.assert_called_once_with(
            self.env.PropertyType.BLUE)


if __name__ == "__main__":
    unittest.main()
