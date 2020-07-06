import unittest

from queue import Queue
from modi.module.input_module.button import Button
from modi.module.module import Module


class TestButton(unittest.TestCase):
    """Tests for 'Button' class."""

    def setUp(self):
        """Set up test fixtures, if any."""
        self.virtual_queue = Queue()
        mock_args = (-1, -1, self.virtual_queue)
        self.button = Button(*mock_args)

    def tearDown(self):
        """Tear down test fixtures, if any."""
        del self.button

    def test_get_clicked(self):
        """Test get_clicked method."""
        _ = self.button.clicked
        self.assertEqual(
            self.virtual_queue.get(),
            Module.request_property(-1, Button.PropertyType.CLICKED))

    def test_get_double_clicked(self):
        """Test get_double_clicked method."""
        _ = self.button.double_clicked
        self.assertEqual(
            self.virtual_queue.get(),
            Module.request_property(-1, Button.PropertyType.DOUBLE_CLICKED))

    def test_get_pressed(self):
        """Test get_pressed method."""
        _ = self.button.pressed
        self.assertEqual(
            self.virtual_queue.get(),
            Module.request_property(-1, Button.PropertyType.PRESSED))

    def test_get_toggled(self):
        """Test get_toggled method."""
        _ = self.button.toggled
        self.assertEqual(
            self.virtual_queue.get(),
            Module.request_property(-1, Button.PropertyType.TOGGLED))


if __name__ == "__main__":
    unittest.main()
