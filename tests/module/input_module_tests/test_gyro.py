import unittest

from unittest import mock

from modi.module.input_module.gyro import Gyro


class TestGyro(unittest.TestCase):
    """Tests for 'Gyro' class."""

    def setUp(self):
        """Set up test fixtures, if any."""
        mock_args = (-1, -1, None)
        self.gyro = Gyro(*mock_args)
        self.gyro._get_property = mock.Mock()

    def tearDown(self):
        """Tear down test fixtures, if any."""
        del self.gyro

    def test_get_roll(self):
        """Test get_roll method."""
        self.gyro.get_roll()
        self.gyro._get_property.assert_called_once_with(
            self.gyro.PropertyType.ROLL)

    def test_get_pitch(self):
        """Test get_pitch method."""
        self.gyro.get_pitch()
        self.gyro._get_property.assert_called_once_with(
            self.gyro.PropertyType.PITCH)

    def test_get_yaw(self):
        """Test get_yaw method."""
        self.gyro.get_yaw()
        self.gyro._get_property.assert_called_once_with(
            self.gyro.PropertyType.YAW)

    def test_get_angular_vel_x(self):
        """Test get_angular_vel_x method."""
        self.gyro.get_angular_vel_x()
        self.gyro._get_property.assert_called_once_with(
            self.gyro.PropertyType.ANGULAR_VEL_X
        )

    def test_get_angular_vel_y(self):
        """Test get_angular_vel_y method."""
        self.gyro.get_angular_vel_y()
        self.gyro._get_property.assert_called_once_with(
            self.gyro.PropertyType.ANGULAR_VEL_Y
        )

    def test_get_angular_vel_z(self):
        """Test get_angular_vel_z method."""
        self.gyro.get_angular_vel_z()
        self.gyro._get_property.assert_called_once_with(
            self.gyro.PropertyType.ANGULAR_VEL_Z
        )

    def test_get_acceleration_x(self):
        """Test get_acceleration_x method."""
        self.gyro.get_acceleration_x()
        self.gyro._get_property.assert_called_once_with(
            self.gyro.PropertyType.ACCELERATION_X
        )

    def test_get_acceleration_y(self):
        """Test get_acceleration_x method."""
        self.gyro.get_acceleration_y()
        self.gyro._get_property.assert_called_once_with(
            self.gyro.PropertyType.ACCELERATION_Y
        )

    def test_get_acceleration_z(self):
        """Test get_acceleration_z method."""
        self.gyro.get_acceleration_z()
        self.gyro._get_property.assert_called_once_with(
            self.gyro.PropertyType.ACCELERATION_Z
        )

    def test_get_vibration(self):
        """Test get_vibration method."""
        self.gyro.get_vibration()
        self.gyro._get_property.assert_called_once_with(
            self.gyro.PropertyType.VIBRATION
        )


if __name__ == "__main__":
    unittest.main()
