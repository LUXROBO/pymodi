import unittest

from unittest import mock

from modi.module.input_module.ir import Ir


class TestIr(unittest.TestCase):
    """Tests for 'Ir' package."""

    def setUp(self):
        """Set up test fixtures, if any."""
        mock_args = (-1, -1, None)
        self.ir = Ir(*mock_args)
        self.ir._get_property = mock.Mock()

    def tearDown(self):
        """Tear down test fixtures, if any."""
        del self.ir

    def test_get_proximity(self):
        """Test get_proximity method."""
        self.ir.get_proximity()
        self.ir._get_property.assert_called_once_with(
            self.ir.PropertyType.PROXIMITY)


if __name__ == "__main__":
    unittest.main()
