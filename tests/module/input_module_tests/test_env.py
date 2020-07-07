import unittest

from modi.module.input_module.env import Env
from queue import Queue


class TestEnv(unittest.TestCase):
    """Tests for 'Env' class."""

    def setUp(self):
        """Set up test fixtures, if any."""
        self.send_q = Queue()
        mock_args = (-1, -1, self.send_q)
        self.env = Env(*mock_args)

    def tearDown(self):
        """Tear down test fixtures, if any."""
        del self.env

    def test_get_temperature(self):
        """Test get_temperature method."""
        _ = self.env.temperature
        self.assertEqual(
            self.send_q.get(),
            Env.request_property(-1, Env.PropertyType.TEMPERATURE)
        )

    def test_get_humidity(self):
        """Test get_humidity method."""
        _ = self.env.humidity
        self.assertEqual(
            self.send_q.get(),
            Env.request_property(-1, Env.PropertyType.HUMIDITY)
        )

    def test_get_brightness(self):
        """Test get_brightness method."""
        _ = self.env.brightness
        self.assertEqual(
            self.send_q.get(),
            Env.request_property(-1, Env.PropertyType.BRIGHTNESS)
        )

    def test_get_red(self):
        """Test get_red method."""
        _ = self.env.red
        self.assertEqual(
            self.send_q.get(),
            Env.request_property(-1, Env.PropertyType.RED)
        )

    def test_get_green(self):
        """Test get_green method."""
        _ = self.env.green
        self.assertEqual(
            self.send_q.get(),
            Env.request_property(-1, Env.PropertyType.GREEN)
        )

    def test_get_blue(self):
        """Test get_blue method."""
        _ = self.env.blue
        self.assertEqual(
            self.send_q.get(),
            Env.request_property(-1, Env.PropertyType.BLUE)
        )


if __name__ == "__main__":
    unittest.main()
