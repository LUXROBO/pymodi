import unittest

from modi.module.output_module.speaker import Speaker
from modi.util.message_util import parse_data, parse_message
from modi.util.miscellaneous import MockConn


class TestSpeaker(unittest.TestCase):
    """Tests for 'Speaker' class."""

    def setUp(self):
        """Set up test fixtures, if any."""
        self.conn = MockConn()
        self.mock_kwargs = [-1, -1, self.conn]
        self.speaker = Speaker(*self.mock_kwargs)

    def tearDown(self):
        """Tear down test fixtures, if any."""
        del self.speaker

    def test_set_tune(self):
        """Test set_tune method."""
        expected_values = (500, 30)
        self.speaker.tune = expected_values
        sent_messages = []
        while self.conn.send_list:
            sent_messages.append(self.conn.send_list.pop())
        self.assertTrue(
            parse_message(
                0x03, 0, -1,
                (Speaker.FREQUENCY, None, self.speaker.prop_samp_freq, None)
            ) in sent_messages
        )
        self.assertTrue(
            parse_message(
                0x03, 0, -1,
                (Speaker.VOLUME, None, self.speaker.prop_samp_freq, None)
            ) in sent_messages
        )
        self.assertTrue(
            parse_message(
                0x04, 16, -1, parse_data(expected_values, 'float')
            ) in sent_messages
        )

    def test_get_tune(self):
        """Test get_tune method with none input."""
        _ = self.speaker.tune
        sent_messages = []
        while self.conn.send_list:
            sent_messages.append(self.conn.send_list.pop())
        self.assertTrue(
            parse_message(
                0x03, 0, -1,
                (Speaker.FREQUENCY, None, self.speaker.prop_samp_freq, None)
            ) in sent_messages)
        self.assertTrue(
            parse_message(
                0x03, 0, -1,
                (Speaker.VOLUME, None, self.speaker.prop_samp_freq, None)
            ) in sent_messages
        )

    def test_set_frequency(self):
        """Test set_frequency method."""
        expecetd_frequency = 50
        self.speaker.frequency = expecetd_frequency
        expected_values = (50, 0)
        sent_messages = []
        while self.conn.send_list:
            sent_messages.append(self.conn.send_list.pop())
        self.assertTrue(
            parse_message(
                0x03, 0, -1,
                (Speaker.FREQUENCY, None, self.speaker.prop_samp_freq, None)
            )
            in sent_messages
        )
        self.assertTrue(
            parse_message(
                0x03, 0, -1,
                (Speaker.VOLUME, None, self.speaker.prop_samp_freq, None)
            ) in sent_messages
        )
        self.assertTrue(
            parse_message(
                0x04, 16, -1,
                parse_data(expected_values, 'float')
            ) in sent_messages
        )

    def test_get_frequency(self):
        """Test get_frequency method with none input."""
        _ = self.speaker.frequency
        self.assertEqual(
            self.conn.send_list[1],
            parse_message(
                0x03, 0, -1,
                (Speaker.FREQUENCY, None, self.speaker.prop_samp_freq, None)
            )
        )

    def test_set_volume(self):
        """Test set_volume method."""
        expected_volume = 50
        expected_values = (1318, 50)
        self.speaker.volume = expected_volume
        sent_messages = []
        while self.conn.send_list:
            sent_messages.append(self.conn.send_list.pop())
        self.assertTrue(
            parse_message(
                0x03, 0, -1,
                (Speaker.FREQUENCY, None, self.speaker.prop_samp_freq, None)
            ) in sent_messages
        )
        self.assertTrue(
            parse_message(
                0x03, 0, -1,
                (Speaker.VOLUME, None, self.speaker.prop_samp_freq, None)
            ) in sent_messages
        )
        self.assertTrue(
            parse_message(
                0x04, 16, -1,
                parse_data(expected_values, 'float')
            ) in sent_messages
        )

    def test_get_volume(self):
        """Test get_volume method with none input."""
        _ = self.speaker.volume
        self.assertEqual(
            self.conn.send_list[0],
            parse_message(
                0x03, 0, -1,
                (Speaker.VOLUME, None, self.speaker.prop_samp_freq, None)
            )
        )

    def test_set_off(self):
        """Test set_off method"""
        expected_values = (0, 0)
        self.speaker.tune = 100, 100
        self.speaker.tune = expected_values
        sent_messages = []
        while self.conn.send_list:
            sent_messages.append(self.conn.send_list.pop())
        self.assertTrue(
            parse_message(
                0x03, 0, -1,
                (Speaker.FREQUENCY, None, self.speaker.prop_samp_freq, None)
            ) in sent_messages
        )
        self.assertTrue(
            parse_message(
                0x03, 0, -1,
                (Speaker.VOLUME, None, self.speaker.prop_samp_freq, None)
            ) in sent_messages
        )
        self.assertTrue(
            parse_message(
                0x04, 16, -1,
                parse_data(expected_values, 'float')
            ) in sent_messages
        )


if __name__ == "__main__":
    unittest.main()
