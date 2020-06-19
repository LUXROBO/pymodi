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
        self.motor._get_property = mock.Mock()
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

        self.motor.set_torque(*expected_values)

        self.assertEqual(
            mock.call(*expected_top_params),
            self.motor._set_property.call_args_list[0]
        )

        self.assertEqual(
            mock.call(*expected_bot_params),
            self.motor._set_property.call_args_list[1]
        )

    @mock.patch.object(Motor, "set_torque")
    def test_set_first_torque(self, mock_set_torque):
        """Test set_first_torque method."""
        expected_torque = 10
        self.motor.set_first_torque(expected_torque)
        mock_set_torque.assert_called_once_with(
            first_torque_value=expected_torque)

    @mock.patch.object(Motor, "set_torque")
    def test_set_second_torque(self, mock_set_torque):
        """Test set_second_torque method."""
        expected_torque = 10
        self.motor.set_second_torque(expected_torque)
        mock_set_torque.assert_called_once_with(
            second_torque_value=expected_torque)

    def test_get_torque(self):
        """Test set_torque method with none input."""
        self.motor.get_torque()
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
        self.motor.get_first_torque()
        self.motor._get_property.assert_called_once_with(
            self.motor.PropertyType.FIRST_TORQUE
        )

    def test_get_second_torque(self):
        """Test get_second_torque method"""
        self.motor.get_second_torque()
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

        self.motor.set_speed(*expected_values)

        self.assertEqual(
            mock.call(*expected_top_params),
            self.motor._set_property.call_args_list[0]
        )

        self.assertEqual(
            mock.call(*expected_bot_params),
            self.motor._set_property.call_args_list[1]
        )

    @mock.patch.object(Motor, "set_speed")
    def test_set_first_speed(self, mock_set_speed):
        """Test set_first_speed method."""
        expected_speed = 10
        self.motor.set_first_speed(expected_speed)
        mock_set_speed.assert_called_once_with(
            first_speed_value=expected_speed)

    @mock.patch.object(Motor, "set_speed")
    def test_set_second_speed(self, mock_set_speed):
        """Test set_second_speed method."""
        expected_speed = 10
        self.motor.set_second_speed(expected_speed)
        mock_set_speed.assert_called_once_with(
            second_speed_value=expected_speed)

    def test_get_speed(self):
        """Test get_speed method with none input."""
        self.motor.get_speed()

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
        self.motor.get_first_speed()
        self.motor._get_property.assert_called_once_with(
            self.motor.PropertyType.FIRST_SPEED
        )

    def test_get_second_speed(self):
        """Test get_second_speed method"""
        self.motor.get_second_speed()
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

        self.motor.set_degree(*expected_values)

        self.assertEqual(
            mock.call(*expected_top_params),
            self.motor._set_property.call_args_list[0]
        )

        self.assertEqual(
            mock.call(*expected_bot_params),
            self.motor._set_property.call_args_list[1]
        )

    @mock.patch.object(Motor, "set_degree")
    def test_set_first_degree(self, mock_set_degree):
        """Test set_first_degree method."""
        expected_degree = 10
        self.motor.set_first_degree(expected_degree)
        mock_set_degree.assert_called_once_with(
            first_degree_value=expected_degree)

    @mock.patch.object(Motor, "set_degree")
    def test_set_second_degree(self, mock_set_degree):
        """Test set_second_degree method."""
        expected_degree = 10
        self.motor.set_second_degree(expected_degree)
        mock_set_degree.assert_called_once_with(
            second_degree_value=expected_degree)

    def test_get_degree(self):
        """Test get_degree method with none input."""
        self.motor.get_degree()

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
        self.motor.get_first_degree()
        self.motor._get_property.assert_called_once_with(
            self.motor.PropertyType.FIRST_DEGREE
        )

    def test_get_second_degree(self):
        """Test get_second_degree method"""
        self.motor.get_second_degree()
        self.motor._get_property.assert_called_once_with(
            self.motor.PropertyType.SECOND_DEGREE
        )


if __name__ == "__main__":
    unittest.main()
