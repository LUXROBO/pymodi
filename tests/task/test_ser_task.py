import unittest
from unittest import mock

from serial.tools.list_ports_common import ListPortInfo
from serial.serialutil import SerialException
from serial import Serial
from modi.task.ser_task import SerTask


class TestSerTask(unittest.TestCase):
    """Tests for 'SerTask' class"""

    def setUp(self):
        """Set up test fixtures, if any."""
        self.mock_kwargs = {"ser_recv_q": None, "ser_send_q": None}
        self.ser_task = SerTask(**self.mock_kwargs)

        def eval_list_modi_ports():
            fake_port = ListPortInfo()
            fake_port.device = "TestDevice"
            return [fake_port]

        self.ser_task._list_modi_ports = mock.Mock(side_effect=eval_list_modi_ports)

    def tearDown(self):
        """Tear down test fixtures, if any."""
        del self.ser_task

    def test_open_conn(self):
        """Test open_conn method"""
        self.assertRaises(SerialException, self.ser_task.open_conn)
        self.assertEqual(self.ser_task.serial.port, "TestDevice")
        self.assertEqual(self.ser_task.serial.baudrate, 921600)

    def test_close_conn(self):
        """Test close_conn method"""
        self.ser_task.set_serial(Serial())
        self.assertRaises(AttributeError, self.ser_task._close_conn)


if __name__ == "__main__":
    unittest.main()
