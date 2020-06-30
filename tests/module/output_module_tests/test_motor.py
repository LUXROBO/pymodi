import unittest
from unittest import mock

from modi.module.output_module.motor import Motor


class TestMotor(unittest.TestCase):
    """Tests for 'Motor' class."""

    def setUp(self):
        """Set up test fixtures, if any."""
        self.mock_kwargs = {"id_": -1, "uuid": -1, "msg_send_q": None}
        self.motor = Motor(**self.mock_kwargs)

        def eval_set_property(id, command_type, data):
            return command_type

        self.motor._set_property = mock.Mock(side_effect=eval_set_property)
        self.motor._get_property = mock.Mock(return_value=0)
        self.motor._msg_send_q = mock.Mock()

    def tearDown(self):
        """Tear down test fixtures, if any."""
        del self.motor

    def test_set_motor_channel(self):
        """Test set_motor_channel method"""
        expected_values = motor_channel, control_mode, control_value = 0, 0, 50
        self.motor.set_motor_channel(*expected_values)

        expected_inv_params = (
            self.mock_kwargs["id_"],
            self.motor.ControlType.CHANNEL,
            (*expected_values, 0),
        )
        self.motor._set_property.assert_called_once_with(*expected_inv_params)

    def test_set_torque(self):
        """Test set_torque method."""
        expected_values = first_torque_value, second_torque_value = 50, 50

        expected_top_params = (
            self.mock_kwargs["id_"],
            self.motor.ControlType.CHANNEL,
            (0, 0, first_torque_value, 0),
        )

        expected_bot_params = (
            self.mock_kwargs["id_"],
            self.motor.ControlType.CHANNEL,
            (1, 0, second_torque_value, 0),
        )

        self.motor.torque = expected_values

        self.assertEqual(
            mock.call(*expected_top_params),
            self.motor._set_property.call_args_list[0]
        )

        self.assertEqual(
            mock.call(*expected_bot_params),
            self.motor._set_property.call_args_list[1]
        )

    def test_set_first_torque(self):
        """Test set_first_torque method."""
        expected_torque = 10
        setter_mock = mock.Mock(wraps=Motor.torque.fset)
        mock_property = Motor.torque.setter(setter_mock)
        with mock.patch.object(Motor, 'torque', mock_property):
            self.motor.first_torque = expected_torque
            setter_mock.assert_called_once_with(
                self.motor, (expected_torque, 0))

    def test_set_second_torque(self):
        """Test set_second_torque method."""
        expected_torque = 10
        setter_mock = mock.Mock(wraps=Motor.torque.fset)
        mock_property = Motor.torque.setter(setter_mock)
        with mock.patch.object(Motor, 'torque', mock_property):
            self.motor.second_torque = expected_torque
            setter_mock.assert_called_once_with(
                self.motor, (0, expected_torque))

    def test_get_torque(self):
        """Test set_torque method with none input."""
        _ = self.motor.torque
        self.assertEqual(
            mock.call(self.motor.PropertyType.FIRST_TORQUE),
            self.motor._get_property.call_args_list[0],
        )
        self.assertEqual(
            mock.call(self.motor.PropertyType.SECOND_TORQUE),
            self.motor._get_property.call_args_list[1],
        )

    def test_get_first_torque(self):
        """Test get_first_torque method"""
        _ = self.motor.first_torque
        self.motor._get_property.assert_called_once_with(
            self.motor.PropertyType.FIRST_TORQUE
        )

    def test_get_second_torque(self):
        """Test get_second_torque method"""
        _ = self.motor.second_torque
        self.motor._get_property.assert_called_once_with(
            self.motor.PropertyType.SECOND_TORQUE
        )

    def test_set_speed(self):
        """Test set_speed method."""
        expected_values = first_speed_value, second_speed_value = 50, 50

        expected_top_params = (
            self.mock_kwargs["id_"],
            self.motor.ControlType.CHANNEL,
            (0, 1, first_speed_value, 0),
        )

        expected_bot_params = (
            self.mock_kwargs["id_"],
            self.motor.ControlType.CHANNEL,
            (1, 1, second_speed_value, 0),
        )

        self.motor.speed = expected_values

        self.assertEqual(
            mock.call(*expected_top_params),
            self.motor._set_property.call_args_list[0]
        )

        self.assertEqual(
            mock.call(*expected_bot_params),
            self.motor._set_property.call_args_list[1]
        )

    def test_set_first_speed(self):
        """Test set_first_speed method."""
        expected_speed = 10
        setter_mock = mock.Mock(wraps=Motor.speed.fset)
        mock_property = Motor.speed.setter(setter_mock)
        with mock.patch.object(Motor, 'speed', mock_property):
            self.motor.first_speed = expected_speed
            setter_mock.assert_called_once_with(
                self.motor, (expected_speed, 0))

    def test_set_second_speed(self):
        """Test set_second_speed method."""
        expected_speed = 10
        setter_mock = mock.Mock(wraps=Motor.speed.fset)
        mock_property = Motor.speed.setter(setter_mock)
        with mock.patch.object(Motor, 'speed', mock_property):
            self.motor.second_speed = expected_speed
            setter_mock.assert_called_once_with(
                self.motor, (0, expected_speed))

    def test_get_speed(self):
        """Test get_speed method with none input."""
        _ = self.motor.speed

        self.assertEqual(
            mock.call(self.motor.PropertyType.FIRST_SPEED),
            self.motor._get_property.call_args_list[0],
        )
        self.assertEqual(
            mock.call(self.motor.PropertyType.SECOND_SPEED),
            self.motor._get_property.call_args_list[1],
        )

    def test_get_first_speed(self):
        """Test get_first_speed method"""
        _ = self.motor.first_speed
        self.motor._get_property.assert_called_once_with(
            self.motor.PropertyType.FIRST_SPEED
        )

    def test_get_second_speed(self):
        """Test get_second_speed method"""
        _ = self.motor.second_speed
        self.motor._get_property.assert_called_once_with(
            self.motor.PropertyType.SECOND_SPEED
        )

    def test_set_degree(self):
        """Test set_degree method."""
        expected_values = first_degree_value, second_degree_value = 50, 50

        expected_top_params = (
            self.mock_kwargs["id_"],
            self.motor.ControlType.CHANNEL,
            (0, 2, first_degree_value, 0),
        )

        expected_bot_params = (
            self.mock_kwargs["id_"],
            self.motor.ControlType.CHANNEL,
            (1, 2, second_degree_value, 0),
        )

        self.motor.degree = expected_values

        self.assertEqual(
            mock.call(*expected_top_params),
            self.motor._set_property.call_args_list[0]
        )

        self.assertEqual(
            mock.call(*expected_bot_params),
            self.motor._set_property.call_args_list[1]
        )

    def test_set_first_degree(self):
        """Test set_first_degree method."""
        expected_degree = 10
        setter_mock = mock.Mock(wraps=Motor.degree.fset)
        mock_property = Motor.degree.setter(setter_mock)
        with mock.patch.object(Motor, 'degree', mock_property):
            self.motor.first_degree = expected_degree
            setter_mock.assert_called_once_with(
                self.motor, (expected_degree, 0))

    def test_set_second_degree(self):
        """Test set_second_degree method."""
        expected_degree = 10
        setter_mock = mock.Mock(wraps=Motor.degree.fset)
        mock_property = Motor.degree.setter(setter_mock)
        with mock.patch.object(Motor, 'degree', mock_property):
            self.motor.second_degree = expected_degree
            setter_mock.assert_called_once_with(
                self.motor, (0, expected_degree))

    def test_get_degree(self):
        """Test get_degree method with none input."""
        _ = self.motor.degree

        self.assertEqual(
            mock.call(self.motor.PropertyType.FIRST_DEGREE),
            self.motor._get_property.call_args_list[0],
        )
        self.assertEqual(
            mock.call(self.motor.PropertyType.SECOND_DEGREE),
            self.motor._get_property.call_args_list[1],
        )

    def test_get_first_degree(self):
        """Test get_first_degree method"""
        _ = self.motor.first_degree
        self.motor._get_property.assert_called_once_with(
            self.motor.PropertyType.FIRST_DEGREE
        )

    def test_get_second_degree(self):
        """Test get_second_degree method"""
        _ = self.motor.second_degree
        self.motor._get_property.assert_called_once_with(
            self.motor.PropertyType.SECOND_DEGREE
        )


if __name__ == "__main__":
    unittest.main()
