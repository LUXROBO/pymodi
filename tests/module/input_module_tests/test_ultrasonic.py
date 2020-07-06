import unittest

from queue import Queue
from modi.module.input_module.ultrasonic import Ultrasonic


class TestUltrasonic(unittest.TestCase):
    """Tests for 'Ultrasonic' class."""

    def setUp(self):
        """Set up test fixtures, if any."""
        self.send_q = Queue()
        mock_args = (-1, -1, self.send_q)
        self.ultrasonic = Ultrasonic(*mock_args)

    def tearDown(self):
        """Tear down test fixtures, if any."""
        del self.ultrasonic

    def test_get_distance(self):
        """Test get_distance method."""
        _ = self.ultrasonic.distance
        self.assertEqual(
            self.send_q.get(),
            Ultrasonic.request_property(-1, Ultrasonic.PropertyType.DISTANCE))


if __name__ == '__main__':
    unittest.main()
