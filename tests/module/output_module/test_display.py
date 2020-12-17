import unittest

from modi.module.output_module.display import Display
from modi.util.message_util import parse_data, parse_message
from modi.util.miscellaneous import MockConn


class TestDisplay(unittest.TestCase):
    """Tests for 'Display' class."""

    def setUp(self):
        """Set up test fixtures, if any."""
        self.conn = MockConn()
        self.mock_kwargs = [-1, -1, self.conn]
        self.display = Display(*self.mock_kwargs)

    def tearDown(self):
        """Tear down test fixtures, if any."""
        del self.display

    def test_set_text(self):
        """Test set_text method."""
        mock_text = "abcd"
        self.display.text = mock_text
        clear_message = parse_message(0x04, 21, -1, (0, 0))
        text_message = parse_message(
            0x04, 17, -1, parse_data(mock_text + '\0', 'string')
        )
        self.assertEqual(
            self.conn.send_list[0],
            clear_message
        )
        self.assertEqual(
            self.conn.send_list[1],
            text_message
        )

    def test_show_variable(self):
        """Test set_variable method."""
        mock_variable = 123
        mock_position = 5
        self.display.show_variable(mock_variable, mock_position, mock_position)
        self.assertEqual(
            self.conn.send_list[0],
            parse_message(0x04, 22, -1, parse_data(
                (mock_variable, mock_position, mock_position), 'display_var'
            ))
        )

    def test_clear(self):
        """Test clear method."""
        self.display.clear()
        clear_message = parse_message(0x04, 21, -1, (0, 0))
        self.assertEqual(self.conn.send_list[0], clear_message)


if __name__ == "__main__":
    unittest.main()
