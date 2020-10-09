import unittest

from modi.module.input_module.env import Env
from modi.util.message_util import parse_message
from modi.util.miscellaneous import MockConn


class TestEnv(unittest.TestCase):
    """Tests for 'Env' class."""

    def setUp(self):
        """Set up test fixtures, if any."""
        self.conn = MockConn()
        mock_args = (-1, -1, self.conn)
        self.env = Env(*mock_args)

    def tearDown(self):
        """Tear down test fixtures, if any."""
        del self.env

    def test_get_temperature(self):
        """Test get_temperature method."""
        _ = self.env.temperature
        self.assertEqual(
            self.conn.send_list[0],
            parse_message(
                0x03, 0, -1,
                (Env.TEMPERATURE, None, self.env.prop_samp_freq, None)
            )
        )

    def test_get_humidity(self):
        """Test get_humidity method."""
        _ = self.env.humidity
        self.assertEqual(
            self.conn.send_list[0],
            parse_message(
                0x03, 0, -1,
                (Env.HUMIDITY, None, self.env.prop_samp_freq, None)
            )
        )

    def test_get_brightness(self):
        """Test get_brightness method."""
        _ = self.env.brightness
        self.assertEqual(
            self.conn.send_list[0],
            parse_message(
                0x03, 0, -1,
                (Env.BRIGHTNESS, None, self.env.prop_samp_freq, None)
            )
        )

    def test_get_red(self):
        """Test get_red method."""
        _ = self.env.red
        self.assertEqual(
            self.conn.send_list[0],
            parse_message(
                0x03, 0, -1,
                (Env.RED, None, self.env.prop_samp_freq, None)
            )
        )

    def test_get_green(self):
        """Test get_green method."""
        _ = self.env.green
        self.assertEqual(
            self.conn.send_list[0],
            parse_message(
                0x03, 0, -1,
                (Env.GREEN, None, self.env.prop_samp_freq, None)
            )
        )

    def test_get_blue(self):
        """Test get_blue method."""
        _ = self.env.blue
        self.assertEqual(
            self.conn.send_list[0],
            parse_message(
                0x03, 0, -1,
                (Env.BLUE, None, self.env.prop_samp_freq, None)
            )
        )


if __name__ == "__main__":
    unittest.main()
