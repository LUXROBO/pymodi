import unittest

from modi.module.input_module.dial import Dial
from modi.util.message_util import parse_message
from modi.util.miscellaneous import MockConn


class TestDial(unittest.TestCase):
    """Tests for 'Dial' class."""

    def setUp(self):
        """Set up test fixtures, if any."""
        self.conn = MockConn()
        mock_args = (-1, -1, self.conn)
        self.dial = Dial(*mock_args)

    def tearDown(self):
        """Tear down test fixtures, if any."""
        del self.dial

    def test_get_degree(self):
        """Test get_degree method."""
        _ = self.dial.degree
        self.assertEqual(
            self.conn.send_list[0],
            parse_message(
                0x03, 0, -1,
                (Dial.DEGREE, None, self.dial.prop_samp_freq, None)
            )
        )

    def test_get_turnspeed(self):
        """Test get_turnspeed method."""
        _ = self.dial.turnspeed
        self.assertEqual(
            self.conn.send_list[0],
            parse_message(
                0x03, 0, -1,
                (Dial.TURNSPEED, None, self.dial.prop_samp_freq, None)
            )
        )


if __name__ == "__main__":
    unittest.main()
