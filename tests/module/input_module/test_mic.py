
import unittest

from modi.module.input_module.mic import Mic
from modi.util.message_util import parse_message
from modi.util.miscellaneous import MockConn


class TestMic(unittest.TestCase):
    """Tests for 'Mic' class."""

    def setUp(self):
        """Set up test fixtures, if any."""
        self.conn = MockConn()
        mock_args = (-1, -1, self.conn)
        self.mic = Mic(*mock_args)

    def tearDown(self):
        """Tear down test fixtures, if any."""
        del self.mic

    def test_get_volume(self):
        """Test get_volume method."""
        _ = self.mic.volume
        self.assertEqual(
            self.conn.send_list[0],
            parse_message(
                0x03, 0, -1,
                (Mic.VOLUME, None, self.mic.prop_samp_freq, None)
            )
        )

    def test_get_frequency(self):
        """Test get_frequency method."""
        _ = self.mic.frequency
        self.assertEqual(
            self.conn.send_list[0],
            parse_message(
                0x03, 0, -1,
                (Mic.FREQUENCY, None, self.mic.prop_samp_freq, None)
            )
        )


if __name__ == '__main__':
    unittest.main()
