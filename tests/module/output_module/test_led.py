import unittest

from modi.module.output_module.led import Led
from modi.util.message_util import parse_data, parse_message
from modi.util.miscellaneous import MockConn


class TestLed(unittest.TestCase):
    """Tests for 'Led' class."""

    def setUp(self):
        """Set up test fixtures, if any."""
        self.conn = MockConn()
        self.mock_kwargs = -1, -1, self.conn
        self.led = Led(*self.mock_kwargs)

    def tearDown(self):
        """Tear down test fixtures, if any."""
        del self.led

    def test_set_rgb(self):
        """Test set_rgb method with user-defined inputs."""
        expected_color = (10, 20, 100)
        self.led.rgb = expected_color
        set_message = parse_message(
            0x04, 16, -1,
            parse_data(expected_color, 'int')
        )
        sent_messages = []
        while self.conn.send_list:
            sent_messages.append(self.conn.send_list.pop())
        self.assertTrue(set_message in sent_messages)

    def test_set_red(self):
        """Test set_red method."""
        expected_color = (20, 0, 0)
        set_message = parse_message(
            0x04, 16, -1,
            parse_data(expected_color, 'int')
        )
        sent_messages = []
        self.led.red = 20
        while self.conn.send_list:
            sent_messages.append(self.conn.send_list.pop())
        self.assertTrue(set_message in sent_messages)

    def test_get_red(self):
        """Test get_red method with none input."""
        _ = self.led.red
        self.assertEqual(
            self.conn.send_list[0],
            parse_message(
                0x03, 0, -1, (Led.RED, None, self.led.prop_samp_freq, None)
            )
        )

    def test_set_green(self):
        """Test set_green method."""
        expected_color = (0, 20, 0)
        set_message = parse_message(
            0x04, 16, -1,
            parse_data(expected_color, 'int')
        )
        sent_messages = []
        self.led.green = 20
        while self.conn.send_list:
            sent_messages.append(self.conn.send_list.pop())
        self.assertTrue(set_message in sent_messages)

    def test_get_green(self):
        """Test set_green method with none input."""
        _ = self.led.green
        self.assertEqual(
            self.conn.send_list[0],
            parse_message(
                0x03, 0, -1,
                (Led.GREEN, None, self.led.prop_samp_freq, None)
            )
        )

    def test_set_blue(self):
        """Test blue method."""
        expected_color = (0, 0, 20)
        set_message = parse_message(
            0x04, 16, -1,
            parse_data(expected_color, 'int')
        )
        sent_messages = []
        self.led.blue = 20
        while self.conn.send_list:
            sent_messages.append(self.conn.send_list.pop())
        self.assertTrue(set_message in sent_messages)

    def test_get_blue(self):
        """Test get blue method with none input."""
        _ = self.led.blue
        self.assertEqual(
            self.conn.send_list[0],
            parse_message(
                0x03, 0, -1,
                (Led.BLUE, None, self.led.prop_samp_freq, None)
            )
        )

    def test_on(self):
        """Test on method."""
        expected_color = (100, 100, 100)
        self.led.rgb = expected_color
        set_message = parse_message(
            0x04, 16, -1,
            parse_data(expected_color, 'int')
        )
        sent_messages = []
        while self.conn.send_list:
            sent_messages.append(self.conn.send_list.pop())
        self.assertTrue(set_message in sent_messages)

    def test_off(self):
        """Test off method."""
        expected_color = (0, 0, 0)
        self.led.turn_on()
        self.led.turn_off()
        set_message = parse_message(
            0x04, 16, -1,
            parse_data(expected_color, 'int')
        )
        sent_messages = []
        while self.conn.send_list:
            sent_messages.append(self.conn.send_list.pop())
        self.assertTrue(set_message in sent_messages)


if __name__ == "__main__":
    unittest.main()
