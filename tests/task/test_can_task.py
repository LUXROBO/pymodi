#import sys
#import json
#import unittest

#from queue import Queue
#from modi.util.message_util import parse_message
#
#if sys.platform == 'linux':
#    from modi.task.can_task import CanTask
#
#
#class MockCan:
#    def __init__(self):
#        self.recv_buffer = Queue()
#
#    def recv(self):
#        json_pkt = parse_message(0x03, 0, 1)
#        return CanTask.compose_can_msg(json.loads(json_pkt))
#
#    def send(self, item):
#        self.recv_buffer.put(item)
#
#
#@unittest.skipUnless(
#    sys.platform == 'linux', reason='CanTask is supported only on Linux'
#)
#class TestCanTask(unittest.TestCase):
#    """Tests for 'CanTask' class"""
#
#    def setUp(self):
#        """Set up test fixtures, if any."""
#        self.can_task = CanTask()
#        self.can_task._bus = MockCan()
#
#    def tearDown(self):
#        """Tear down test fixtures, if any."""
#        del self.can_task
#        CanTask._instances.clear()
#
#    def test_recv(self):
#        """Test _recv_data method"""
#        self.assertEqual(self.can_task.recv(), parse_message(0x03, 0, 1))
#
#    def test_send(self):
#        """Test _send_data method"""
#        json_pkt = parse_message(0x03, 0, 1)
#        self.can_task.send(json_pkt)
#        self.assertEqual(
#            self.can_task.bus.recv_buffer.get().data,
#            CanTask.compose_can_msg(json.loads(json_pkt)).data
#        )
#
#
#if __name__ == "__main__":
#    unittest.main()
#
