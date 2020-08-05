import unittest

from modi.module.input_module.gyro import Gyro
from modi.util.msgutil import parse_message
from modi.util.misc import MockConn


class TestGyro(unittest.TestCase):
    """Tests for 'Gyro' class."""

    def setUp(self):
        """Set up test fixtures, if any."""
        self.conn = MockConn()
        mock_args = (-1, -1, self.conn)
        self.gyro = Gyro(*mock_args)

    def tearDown(self):
        """Tear down test fixtures, if any."""
        del self.gyro

    def test_get_roll(self):
        """Test get_roll method."""
        _ = self.gyro.roll
        self.assertEqual(
            self.conn.send_list[0],
            parse_message(0x03, 0, -1,
                          (Gyro.PropertyType.ROLL, None, 95, None))
        )

    def test_get_pitch(self):
        """Test get_pitch method."""
        _ = self.gyro.pitch
        self.assertEqual(
            self.conn.send_list[0],
            parse_message(0x03, 0, -1,
                          (Gyro.PropertyType.PITCH, None, 95, None))
        )

    def test_get_yaw(self):
        """Test get_yaw method."""
        _ = self.gyro.yaw
        self.assertEqual(
            self.conn.send_list[0],
            parse_message(0x03, 0, -1,
                          (Gyro.PropertyType.YAW, None, 95, None))
        )

    def test_get_angular_vel_x(self):
        """Test get_angular_vel_x method."""
        _ = self.gyro.angular_vel_x
        self.assertEqual(
            self.conn.send_list[0],
            parse_message(0x03, 0, -1,
                          (Gyro.PropertyType.ANGULAR_VEL_X, None, 95, None))
        )

    def test_get_angular_vel_y(self):
        """Test get_angular_vel_y method."""
        _ = self.gyro.angular_vel_y
        self.assertEqual(
            self.conn.send_list[0],
            parse_message(0x03, 0, -1,
                          (Gyro.PropertyType.ANGULAR_VEL_Y, None, 95, None))
        )

    def test_get_angular_vel_z(self):
        """Test get_angular_vel_z method."""
        _ = self.gyro.angular_vel_z
        self.assertEqual(
            self.conn.send_list[0],
            parse_message(0x03, 0, -1,
                          (Gyro.PropertyType.ANGULAR_VEL_Z, None, 95, None))
        )

    def test_get_acceleration_x(self):
        """Test get_acceleration_x method."""
        _ = self.gyro.acceleration_x
        self.assertEqual(
            self.conn.send_list[0],
            parse_message(0x03, 0, -1,
                          (Gyro.PropertyType.ACCELERATION_X, None, 95, None))
        )

    def test_get_acceleration_y(self):
        """Test get_acceleration_x method."""
        _ = self.gyro.acceleration_y
        self.assertEqual(
            self.conn.send_list[0],
            parse_message(0x03, 0, -1,
                          (Gyro.PropertyType.ACCELERATION_Y, None, 95, None))
        )

    def test_get_acceleration_z(self):
        """Test get_acceleration_z method."""
        _ = self.gyro.acceleration_z
        self.assertEqual(
            self.conn.send_list[0],
            parse_message(0x03, 0, -1,
                          (Gyro.PropertyType.ACCELERATION_Z, None, 95, None))
        )

    def test_get_vibration(self):
        """Test get_vibration method."""
        _ = self.gyro.vibration
        self.assertEqual(
            self.conn.send_list[0],
            parse_message(0x03, 0, -1,
                          (Gyro.PropertyType.VIBRATION, None, 95, None))
        )


if __name__ == "__main__":
    unittest.main()
