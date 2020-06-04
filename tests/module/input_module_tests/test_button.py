import unittest

from unittest import mock

from modi.module.input_module.button import Button


class TestButton(unittest.TestCase):
    """Tests for 'Button' class."""

    def setUp(self):
        """Set up test fixtures, if any."""
        mock_args = (-1, -1, None)
        self.button = Button(*mock_args)
        self.button._get_property = mock.Mock()

    def tearDown(self):
        """Tear down test fixtures, if any."""
        del self.button

    def test_get_clicked(self):
        """Test get_clicked method."""
        self.button.get_clicked()
        self.button._get_property.assert_called_once_with(
            self.button.PropertyType.CLICKED
        )

    def test_get_double_clicked(self):
        """Test get_double_clicked method."""
        self.button.get_double_clicked()
        self.button._get_property.assert_called_once_with(
            self.button.PropertyType.DOUBLE_CLICKED
        )

    def test_get_pressed(self):
        """Test get_pressed method."""
        self.button.get_pressed()
        self.button._get_property.assert_called_once_with(
            self.button.PropertyType.PRESSED
        )

    def test_get_toggled(self):
        """Test get_toggled method."""
        self.button.get_toggled()
        self.button._get_property.assert_called_once_with(
            self.button.PropertyType.TOGGLED
        )


if __name__ == "__main__":
    unittest.main()
