import unittest

from modi.module.output_module.motor import Motor
from modi.util.msgutil import parse_data, parse_message
from modi.util.misc import MockConn


class TestMotor(unittest.TestCase):
    """Tests for 'Motor' class."""

    def setUp(self):
        """Set up test fixtures, if any."""
        self.conn = MockConn()
        self.mock_kwargs = [-1, -1, self.conn]
        self.motor = Motor(*self.mock_kwargs)

    def tearDown(self):
        """Tear down test fixtures, if any."""
        del self.motor

    def test_set_motor_channel(self):
        """Test set_motor_channel method"""
        expected_values = motor_channel, control_mode, control_value = 0, 0, 50
        self.motor.set_motor_channel(*expected_values)
        self.assertEqual(
            self.conn.send_list[0],
            parse_message(0x04, 19, -1, parse_data(
                (motor_channel, control_mode, control_value), 'int'))
        )

    def test_set_torque(self):
        """Test set_torque method."""
        expected_values = first_torque_value, second_torque_value = 50, 50
        self.motor.torque = expected_values
        sent_messages = []
        while self.conn.send_list:
            sent_messages.append(self.conn.send_list.pop())
        self.assertTrue(
            parse_message(0x03, 0, -1, (Motor.PropertyType.FIRST_TORQUE,
                                        None, 95, None))
            in sent_messages)
        self.assertTrue(
            parse_message(0x03, 0, -1, (Motor.PropertyType.SECOND_TORQUE,
                                        None, 95, None))
            in sent_messages)
        self.assertTrue(
            parse_message(0x04, 16, -1, parse_data(
                expected_values, 'int'
            )) in sent_messages)

    def test_set_first_torque(self):
        """Test set_first_torque method."""
        first_torque_value = 50
        self.motor.first_torque = first_torque_value
        sent_messages = []
        while self.conn.send_list:
            sent_messages.append(self.conn.send_list.pop())
        self.assertTrue(
            parse_message(0x03, 0, -1, (Motor.PropertyType.FIRST_TORQUE,
                                        None, 95, None))
            in sent_messages)
        self.assertTrue(
            parse_message(0x04, 16, -1, parse_data(
                (first_torque_value, 0), 'int'
            )) in sent_messages)

    def test_set_second_torque(self):
        """Test set_second_torque method."""
        second_torque_value = 50
        self.motor.second_torque = second_torque_value
        sent_messages = []
        while self.conn.send_list:
            sent_messages.append(self.conn.send_list.pop())
        self.assertTrue(
            parse_message(0x03, 0, -1, (Motor.PropertyType.SECOND_TORQUE,
                                        None, 95, None))
            in sent_messages)
        self.assertTrue(
            parse_message(0x04, 16, -1, parse_data(
                (0, second_torque_value), 'int'
            )) in sent_messages)

    def test_get_torque(self):
        """Test set_torque method with none input."""
        _ = self.motor.torque
        sent_messages = []
        while self.conn.send_list:
            sent_messages.append(self.conn.send_list.pop())
        self.assertTrue(
            parse_message(0x03, 0, -1, (Motor.PropertyType.FIRST_TORQUE,
                                        None, 95, None))
            in sent_messages)
        self.assertTrue(
            parse_message(0x03, 0, -1, (Motor.PropertyType.SECOND_TORQUE,
                                        None, 95, None))
            in sent_messages)

    def test_get_first_torque(self):
        """Test get_first_torque method"""
        _ = self.motor.first_torque
        sent_messages = []
        while self.conn.send_list:
            sent_messages.append(self.conn.send_list.pop())
        self.assertTrue(
            parse_message(0x03, 0, -1, (Motor.PropertyType.FIRST_TORQUE,
                                        None, 95, None))
            in sent_messages)

    def test_get_second_torque(self):
        """Test get_second_torque method"""
        _ = self.motor.second_torque
        sent_messages = []
        while self.conn.send_list:
            sent_messages.append(self.conn.send_list.pop())
        self.assertTrue(
            parse_message(0x03, 0, -1, (Motor.PropertyType.SECOND_TORQUE,
                                        None, 95, None))
            in sent_messages)

    def test_set_speed(self):
        """Test set_speed method."""
        expected_values = first_speed_value, second_speed_value = 50, 50
        self.motor.speed = expected_values
        sent_messages = []
        while self.conn.send_list:
            sent_messages.append(self.conn.send_list.pop())
        self.assertTrue(
            parse_message(0x03, 0, -1, (Motor.PropertyType.FIRST_SPEED,
                                        None, 95, None))
            in sent_messages)
        self.assertTrue(
            parse_message(0x03, 0, -1, (Motor.PropertyType.SECOND_SPEED,
                                        None, 95, None))
            in sent_messages)
        self.assertTrue(
            parse_message(0x04, 19, -1, parse_data(
                (0, 1, first_speed_value), 'int'
            )) in sent_messages)
        self.assertTrue(
            parse_message(0x04, 19, -1, parse_data(
                (1, 1, second_speed_value), 'int'
            )) in sent_messages)

    def test_set_first_speed(self):
        """Test set_first_speed method."""
        first_speed_value = 50
        self.motor.first_speed = first_speed_value
        sent_messages = []
        while self.conn.send_list:
            sent_messages.append(self.conn.send_list.pop())
        self.assertTrue(
            parse_message(0x03, 0, -1, (Motor.PropertyType.FIRST_SPEED,
                                        None, 95, None))
            in sent_messages)
        self.assertTrue(
            parse_message(0x04, 19, -1, parse_data(
                (0, 1, first_speed_value), 'int'
            )) in sent_messages)

    def test_set_second_speed(self):
        """Test set_second_speed method."""
        second_speed_value = 50
        self.motor.second_speed = second_speed_value
        sent_messages = []
        while self.conn.send_list:
            sent_messages.append(self.conn.send_list.pop())
        self.assertTrue(
            parse_message(0x03, 0, -1, (Motor.PropertyType.SECOND_SPEED,
                                        None, 95, None))
            in sent_messages)
        self.assertTrue(
            parse_message(0x04, 19, -1, parse_data(
                (1, 1, second_speed_value), 'int'
            )) in sent_messages)

    def test_get_speed(self):
        """Test get_speed method with none input."""
        _ = self.motor.speed
        sent_messages = []
        while self.conn.send_list:
            sent_messages.append(self.conn.send_list.pop())
        self.assertTrue(
            parse_message(0x03, 0, -1, (Motor.PropertyType.FIRST_SPEED,
                                        None, 95, None))
            in sent_messages)
        self.assertTrue(
            parse_message(0x03, 0, -1, (Motor.PropertyType.SECOND_SPEED,
                                        None, 95, None))
            in sent_messages)

    def test_get_first_speed(self):
        """Test get_first_speed method"""
        _ = self.motor.first_speed
        sent_messages = []
        while self.conn.send_list:
            sent_messages.append(self.conn.send_list.pop())
        self.assertTrue(
            parse_message(0x03, 0, -1, (Motor.PropertyType.FIRST_SPEED,
                                        None, 95, None))
            in sent_messages)

    def test_get_second_speed(self):
        """Test get_second_speed method"""
        _ = self.motor.second_speed
        sent_messages = []
        while self.conn.send_list:
            sent_messages.append(self.conn.send_list.pop())
        self.assertTrue(
            parse_message(0x03, 0, -1, (Motor.PropertyType.SECOND_SPEED,
                                        None, 95, None))
            in sent_messages)

    def test_set_degree(self):
        """Test set_degree method."""
        expected_values = first_degree_value, second_degree_value = 50, 50
        self.motor.degree = expected_values
        sent_messages = []
        while self.conn.send_list:
            sent_messages.append(self.conn.send_list.pop())
        self.assertTrue(
            parse_message(0x03, 0, -1, (Motor.PropertyType.FIRST_DEGREE,
                                        None, 95, None))
            in sent_messages)
        self.assertTrue(
            parse_message(0x03, 0, -1, (Motor.PropertyType.SECOND_DEGREE,
                                        None, 95, None))
            in sent_messages)
        self.assertTrue(
            parse_message(0x04, 19, -1, parse_data(
                (0, 2, first_degree_value), 'int'
            )) in sent_messages)
        self.assertTrue(
            parse_message(0x04, 19, -1, parse_data(
                (1, 2, second_degree_value), 'int'
            )) in sent_messages)

    def test_set_first_degree(self):
        """Test set_first_degree method."""
        first_degree_value = 50
        self.motor.first_degree = first_degree_value
        sent_messages = []
        while self.conn.send_list:
            sent_messages.append(self.conn.send_list.pop())
        self.assertTrue(
            parse_message(0x03, 0, -1, (Motor.PropertyType.FIRST_DEGREE,
                                        None, 95, None))
            in sent_messages)
        self.assertTrue(
            parse_message(0x04, 19, -1, parse_data(
                (0, 2, first_degree_value), 'int'
            )) in sent_messages)

    def test_set_second_degree(self):
        """Test set_second_degree method."""
        second_degree_value = 50
        self.motor.second_degree = second_degree_value
        sent_messages = []
        while self.conn.send_list:
            sent_messages.append(self.conn.send_list.pop())
        self.assertTrue(
            parse_message(0x03, 0, -1, (Motor.PropertyType.SECOND_DEGREE,
                                        None, 95, None))
            in sent_messages)
        self.assertTrue(
            parse_message(0x04, 19, -1, parse_data(
                (1, 2, second_degree_value), 'int'
            )) in sent_messages)

    def test_get_degree(self):
        """Test get_degree method with none input."""
        _ = self.motor.degree
        sent_messages = []
        while self.conn.send_list:
            sent_messages.append(self.conn.send_list.pop())
        self.assertTrue(
            parse_message(0x03, 0, -1, (Motor.PropertyType.FIRST_DEGREE,
                                        None, 95, None))
            in sent_messages)
        self.assertTrue(
            parse_message(0x03, 0, -1, (Motor.PropertyType.SECOND_DEGREE,
                                        None, 95, None))
            in sent_messages)

    def test_get_first_degree(self):
        """Test get_first_degree method"""
        _ = self.motor.first_degree
        sent_messages = []
        while self.conn.send_list:
            sent_messages.append(self.conn.send_list.pop())
        self.assertTrue(
            parse_message(0x03, 0, -1, (Motor.PropertyType.FIRST_DEGREE,
                                        None, 95, None))
            in sent_messages)

    def test_get_second_degree(self):
        """Test get_second_degree method"""
        _ = self.motor.second_degree
        sent_messages = []
        while self.conn.send_list:
            sent_messages.append(self.conn.send_list.pop())
        self.assertTrue(
            parse_message(0x03, 0, -1, (Motor.PropertyType.SECOND_DEGREE,
                                        None, 95, None))
            in sent_messages)


if __name__ == "__main__":
    unittest.main()
