import unittest

from queue import Queue
from modi.module.input_module.ir import Ir


class TestIr(unittest.TestCase):
    """Tests for 'Ir' package."""

    def setUp(self):
        """Set up test fixtures, if any."""
        self.send_q = Queue()
        mock_args = (-1, -1, self.send_q)
        self.ir = Ir(*mock_args)

    def tearDown(self):
        """Tear down test fixtures, if any."""
        del self.ir

    def test_get_proximity(self):
        """Test get_proximity method."""
        _ = self.ir.proximity
        self.assertEqual(
            self.send_q.get(),
            Ir.request_property(-1, Ir.PropertyType.PROXIMITY))


if __name__ == "__main__":
    unittest.main()
