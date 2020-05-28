import unittest

from unittest import mock

from queue import Queue
from serial.tools.list_ports_common import ListPortInfo
from serial.serialutil import SerialException
from modi.task.ser_task import SerTask


class TestSerTask(unittest.TestCase):
    """Tests for 'SerTask' class"""
    class MockSerial:
        def __init__(self):
            self.in_waiting = 1
            self.read = mock.Mock(return_value=bytes(1))
            self.write = mock.Mock()
            self.close = mock.Mock()

    def setUp(self):
        """Set up test fixtures, if any."""
        self.mock_kwargs = {"ser_recv_q": Queue(), "ser_send_q": Queue()}
        self.ser_task = SerTask(**self.mock_kwargs)

        def eval_list_modi_ports():
            fake_port = ListPortInfo()
            fake_port.device = "TestDevice"
            return [fake_port]

        self.ser_task._list_modi_ports = mock.Mock(
            side_effect=eval_list_modi_ports)

    def tearDown(self):
        """Tear down test fixtures, if any."""
        del self.ser_task

    def test_open_conn(self):
        """Test open_conn method"""
        self.assertRaises(SerialException, self.ser_task.open_conn)
        self.assertEqual(self.ser_task.get_serial.port, "TestDevice")
        self.assertEqual(self.ser_task.get_serial.baudrate, 921600)

    def test_close_conn(self):
        """Test close_conn method"""
        self.ser_task.set_serial(self.MockSerial())
        self.ser_task._close_conn()
        self.ser_task.get_serial.close.assert_called_once_with()

    def test_read_data(self):
        """Test _read_data method"""
        self.ser_task.set_serial(self.MockSerial())
        self.ser_task._read_data()
        self.ser_task.get_serial.read.assert_called_once_with(1)

    def test_write_data(self):
        """Test _write_data method"""
        self.ser_task.set_serial(self.MockSerial())
        self.ser_task._ser_send_q.put("foo")
        self.ser_task._write_data()
        self.ser_task.get_serial.write.assert_called_once_with("foo".encode())


if __name__ == "__main__":
    unittest.main()
