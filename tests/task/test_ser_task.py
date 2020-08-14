import unittest

from unittest import mock

from modi.task.ser_task import SerTask


class TestSerTask(unittest.TestCase):
    """Tests for 'SerTask' class"""
    class MockSerial:
        def __init__(self):
            self.in_waiting = 1
            self.read_all = mock.Mock(side_effect=self.read_mock)
            self.write = mock.Mock()
            self.close = mock.Mock()

        def read_mock(self):
            self.in_waiting = 0
            return b'{complete}'

    def setUp(self):
        """Set up test fixtures, if any."""
        self.ser_task = SerTask()

    def tearDown(self):
        """Tear down test fixtures, if any."""
        del self.ser_task

    def test_close_conn(self):
        """Test close_conn method"""
        self.ser_task._bus = self.MockSerial()
        self.ser_task.close_conn()
        self.ser_task.bus.close.assert_called_once_with()

    def test_recv_data(self):
        """Test _read_data method"""
        self.ser_task._bus = self.MockSerial()
        self.assertEqual(self.ser_task.recv(), '{complete}')

    def test_send_data(self):
        """Test _write_data method"""
        self.ser_task._bus = self.MockSerial()
        self.ser_task.send("foo")
        self.ser_task.bus.write.assert_called_once_with("foo".encode())


if __name__ == "__main__":
    unittest.main()
