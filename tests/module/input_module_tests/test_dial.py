import unittest

from queue import Queue
from modi.module.input_module.dial import Dial
from modi.module.module import Module


class TestDial(unittest.TestCase):
    """Tests for 'Dial' class."""

    def setUp(self):
        """Set up test fixtures, if any."""
        self.send_q = Queue()
        mock_args = (-1, -1, self.send_q)
        self.dial = Dial(*mock_args)

    def tearDown(self):
        """Tear down test fixtures, if any."""
        del self.dial

    def test_get_degree(self):
        """Test get_degree method."""
        _ = self.dial.degree
        self.assertEqual(
            self.send_q.get(),
            Module.request_property(-1, Dial.PropertyType.DEGREE)
        )

    def test_get_turnspeed(self):
        """Test get_turnspeed method."""
        _ = self.dial.turnspeed
        self.assertEqual(
            self.send_q.get(),
            Module.request_property(-1, Dial.PropertyType.TURNSPEED)
        )


if __name__ == "__main__":
    unittest.main()
