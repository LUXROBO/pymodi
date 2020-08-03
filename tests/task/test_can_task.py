import json
import unittest

from queue import Queue
from modi.task.can_task import CanTask
from modi.task.conn_task import ConnTask
from modi.util.msgutil import parse_message


class MockCan:
    def __init__(self):
        self.recv_buffer = Queue()

    def recv(self, timeout):
        json_pkt = parse_message(0x03, 0, 1)
        return CanTask.compose_can_msg(json.loads(json_pkt))

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
        CanTask._instances.clear()

    def test_open_conn(self):
        """Test open_conn method"""
        if not ConnTask.is_on_pi():
            print("Aborting test on non-pi environment..")
            return
        else:
            self.can_task.open_conn()

    def test_recv_data(self):
        """Test _recv_data method"""
        self.can_task._recv_data()
        self.assertEqual(self.recv_q.get(), parse_message(0x03, 0, 1))

    def test_send_data(self):
        """Test _send_data method"""
        json_pkt = parse_message(0x03, 0, 1)
        self.send_q.put(json_pkt)
        self.can_task._send_data()
        self.assertEqual(self.can_task.can0.recv_buffer.get().data,
                         CanTask.compose_can_msg(json.loads(json_pkt)).data
                         )


if __name__ == "__main__":
    unittest.main()
