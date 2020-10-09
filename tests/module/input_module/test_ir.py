import unittest

from modi.module.input_module.ir import Ir
from modi.util.message_util import parse_message
from modi.util.miscellaneous import MockConn


class TestIr(unittest.TestCase):
    """Tests for 'Ir' package."""

    def setUp(self):
        """Set up test fixtures, if any."""
        self.conn = MockConn()
        mock_args = (-1, -1, self.conn)
        self.ir = Ir(*mock_args)

    def tearDown(self):
        """Tear down test fixtures, if any."""
        del self.ir

    def test_get_proximity(self):
        """Test get_proximity method."""
        _ = self.ir.proximity
        self.assertEqual(
            self.conn.send_list[0],
            parse_message(
                0x03, 0, -1,
                (Ir.PROXIMITY, None, self.ir.prop_samp_freq, None)
            )
        )


if __name__ == "__main__":
    unittest.main()
