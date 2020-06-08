import unittest

from unittest import mock

from queue import Queue
from serial.tools.list_ports_common import ListPortInfo
from serial.serialutil import SerialException
from modi.task.spp_task import SppTask


class TestSppTask(unittest.TestCase):
    """Tests for 'SppTask' class"""
    class MockSerial:
        def __init__(self):
            self.in_waiting = 1
            self.read = mock.Mock(return_value=bytes(1))
            self.write = mock.Mock()
            self.close = mock.Mock()

    def setUp(self):
        """Set up test fixtures, if any."""
        self.mock_kwargs = {'spp_recv_q': Queue(), 'spp_send_q': Queue(),
                            'module_uuid': None}
        self.spp_task = SppTask(**self.mock_kwargs)

        def eval_list_modi_ports():
            fake_port = ListPortInfo()
            fake_port.device = "TestDevice"
            return [fake_port]

        self.spp_task._list_modi_ports = mock.Mock(
            side_effect=eval_list_modi_ports)

    def tearDown(self):
        """Tear down test fixtures, if any."""
        del self.spp_task

    def test_open_conn(self):
        """Test open_conn method"""
        self.assertRaises(SerialException, self.spp_task.open_conn)
        self.assertEqual(self.spp_task.get_serial.port, "TestDevice")
        self.assertEqual(self.spp_task.get_serial.baudrate, 921600)

    def test_close_conn(self):
        """Test close_conn method"""
        self.spp_task.set_serial(self.MockSerial())
        self.spp_task._close_conn()
        self.spp_task.get_serial.close.assert_called_once_with()

    def test_recv_data(self):
        """Test _read_data method"""
        self.spp_task.set_serial(self.MockSerial())
        self.spp_task._recv_data()
        self.spp_task.get_serial.read.assert_called_once_with(1)

    def test_send_data(self):
        """Test _write_data method"""
        self.spp_task.set_serial(self.MockSerial())
        self.spp_task._spp_send_q.put("foo")
        self.spp_task._send_data()
        self.spp_task.get_serial.write.assert_called_once_with("foo".encode())


if __name__ == "__main__":
    unittest.main()
