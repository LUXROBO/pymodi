
import unittest

from queue import Queue
from modi.module.input_module.mic import Mic


class TestMic(unittest.TestCase):
    """Tests for 'Mic' class."""

    def setUp(self):
        """Set up test fixtures, if any."""
        self.send_q = Queue()
        mock_args = (-1, -1, self.send_q)
        self.mic = Mic(*mock_args)

    def tearDown(self):
        """Tear down test fixtures, if any."""
        del self.mic

    def test_get_volume(self):
        """Test get_volume method."""
        _ = self.mic.volume
        self.assertEqual(
            self.send_q.get(),
            Mic.request_property(-1, Mic.PropertyType.VOLUME))

    def test_get_frequency(self):
        """Test get_frequency method."""
        _ = self.mic.frequency
        self.assertEqual(
            self.send_q.get(),
            Mic.request_property(-1, Mic.PropertyType.FREQUENCY))


if __name__ == '__main__':
    unittest.main()
