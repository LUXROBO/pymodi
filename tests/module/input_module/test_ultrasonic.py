import unittest

from modi.module.input_module.ultrasonic import Ultrasonic
from modi.util.message_util import parse_message
from modi.util.miscellaneous import MockConn


class TestUltrasonic(unittest.TestCase):
    """Tests for 'Ultrasonic' class."""

    def setUp(self):
        """Set up test fixtures, if any."""
        self.conn = MockConn()
        mock_args = (-1, -1, self.conn)
        self.ultrasonic = Ultrasonic(*mock_args)

    def tearDown(self):
        """Tear down test fixtures, if any."""
        del self.ultrasonic

    def test_get_distance(self):
        """Test get_distance method."""
        _ = self.ultrasonic.distance
        self.assertEqual(
            self.conn.send_list[0],
            parse_message(
                0x03, 0, -1,
                (
                    Ultrasonic.DISTANCE,
                    None,
                    self.ultrasonic.prop_samp_freq,
                    None
                )
            )
        )


if __name__ == '__main__':
    unittest.main()
