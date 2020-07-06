import unittest

from queue import Queue
from modi.module.output_module.display import Display
from modi.util.msgutil import parse_data, parse_message


class TestDisplay(unittest.TestCase):
    """Tests for 'Display' class."""

    def setUp(self):
        """Set up test fixtures, if any."""
        self.send_q = Queue()
        self.mock_kwargs = {"id_": -1, "uuid": -1, "msg_send_q": self.send_q}
        self.display = Display(**self.mock_kwargs)

    def tearDown(self):
        """Tear down test fixtures, if any."""
        del self.display

    def test_set_text(self):
        """Test set_text method."""
        mock_text = "abcd"
        self.display.text = mock_text
        clear_message = parse_message(0x04, 21, -1, (0, 0))
        text_message = parse_message(0x04, 17, -1, parse_data(mock_text,
                                                              'string'))
        self.assertEqual(
            self.send_q.get(),
            clear_message
        )
        self.assertEqual(
            self.send_q.get(),
            text_message
        )

    def test_show_variable(self):
        """Test set_variable method."""
        mock_variable = 123
        mock_position = 5
        self.display.show_variable(mock_variable, mock_position, mock_position)
        self.assertEqual(
            self.send_q.get(),
            parse_message(0x04, 22, -1, parse_data(
                (mock_variable, mock_position, mock_position), 'display_var'
            ))
        )

    def test_clear(self):
        """Test clear method."""
        self.display.clear()
        clear_message = parse_message(0x04, 21, -1, (0, 0))
        self.assertEqual(
            self.send_q.get(),
            clear_message
        )


if __name__ == "__main__":
    unittest.main()
