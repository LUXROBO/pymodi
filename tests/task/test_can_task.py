import unittest

from queue import Queue
from modi.task.can_task import CanTask
from modi.util.conn_util import is_on_pi
from modi.util.msgutil import parse_message


class MockCan:
    def __init__(self):
        self.recv_buffer = Queue()

    def recv(self, timeout):
        return "Can Message"

    def send(self, item):
        self.recv_buffer.put(item)


class TestCanTask(unittest.TestCase):
    """Tests for 'CanTask' class"""

    def setUp(self):
        """Set up test fixtures, if any."""
        self.send_q, self.recv_q = Queue(), Queue()
        self.mock_kwargs = {"can_recv_q": self.recv_q,
                            "can_send_q": self.send_q,
                            "verbose": False}
        self.can_task = CanTask(**self.mock_kwargs)
        self.can_task.can0 = MockCan()

    def tearDown(self):
        """Tear down test fixtures, if any."""
        del self.can_task

    def test_open_conn(self):
        """Test open_conn method"""
        if not is_on_pi():
            print("Aborting test on non-pi environment..")
            return
        else:
            self.can_task.open_conn()

    def test_recv_data(self):
        """Test _recv_data method"""
        self.assertEqual(
            self.can_task._recv_data(), "Can Message"
        )

    def test_send_data(self):
        """Test _send_data method"""
        self.can_task._send_data(parse_message(0x04, 2, 2, (20, 40)))
        data = self.can_task.can0.recv_buffer.get().data
        self.assertEqual(data[0], 20)
        self.assertEqual(data[1], 40)


if __name__ == "__main__":
    unittest.main()
