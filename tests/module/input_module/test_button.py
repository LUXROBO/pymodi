import unittest

from modi.module.input_module.button import Button
from modi.util.message_util import parse_message
from modi.util.miscellaneous import MockConn


class TestButton(unittest.TestCase):
    """Tests for 'Button' class."""

    def setUp(self):
        """Set up test fixtures, if any."""
        self.conn = MockConn()
        mock_args = (-1, -1, self.conn)
        self.button = Button(*mock_args)

    def tearDown(self):
        """Tear down test fixtures, if any."""
        del self.button

    def test_get_clicked(self):
        """Test get_clicked method."""
        _ = self.button.clicked
        self.assertEqual(
            self.conn.send_list[0],
            parse_message(
                0x03, 0, -1,
                (Button.CLICKED, None, self.button.prop_samp_freq, None)
            )
        )

    def test_get_double_clicked(self):
        """Test get_double_clicked method."""
        _ = self.button.double_clicked
        self.assertEqual(
            self.conn.send_list[0],
            parse_message(
                0x03, 0, -1,
                (Button.DOUBLE_CLICKED, None, self.button.prop_samp_freq, None)
            )
        )

    def test_get_pressed(self):
        """Test get_pressed method."""
        _ = self.button.pressed
        self.assertEqual(
            self.conn.send_list[0],
            parse_message(
                0x03, 0, -1,
                (Button.PRESSED, None, self.button.prop_samp_freq, None)
            )
        )

    def test_get_toggled(self):
        """Test get_toggled method."""
        _ = self.button.toggled
        self.assertEqual(
            self.conn.send_list[0],
            parse_message(
                0x03, 0, -1,
                (Button.TOGGLED, None, self.button.prop_samp_freq, None)
            )
        )


if __name__ == "__main__":
    unittest.main()
