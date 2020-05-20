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
            self.motor.ControlType.INV.value,
            (*expected_values, 0),
        )
        self.motor._set_property.assert_called_once_with(*expected_inv_params)

    def test_set_torque(self):
        """Test set_torque method."""
        expected_values = first_torque_value, second_torque_value = 50, 50
        self.motor.set_torque(*expected_values)

        expected_torque_params = (
            self.mock_kwargs["id_"],
            self.motor.ControlType.TORQUE.value,
            (*expected_values, 0),
        )
        self.motor._set_property.assert_called_once_with(*expected_torque_params)

        self.assertEqual(
            mock.call(self.motor.PropertyType.FIRST_TORQUE),
            self.motor._get_property.call_args_list[0],
        )
        self.assertEqual(
            mock.call(self.motor.PropertyType.SECOND_TORQUE),
            self.motor._get_property.call_args_list[1],
        )

    def test_set_torque_with_none(self):
        """Test set_torque method with none input."""
        self.motor.set_torque()
        self.assertEqual(
            mock.call(self.motor.PropertyType.FIRST_TORQUE),
            self.motor._get_property.call_args_list[0],
        )
        self.assertEqual(
            mock.call(self.motor.PropertyType.SECOND_TORQUE),
            self.motor._get_property.call_args_list[1],
        )

    def test_set_speed(self):
        """Test set_speed method."""
        expected_values = first_speed_value, second_speed_value = 50, 50
        self.motor.set_speed(*expected_values)

        expected_speed_params = (
            self.mock_kwargs["id_"],
            self.motor.ControlType.SPEED.value,
            (first_speed_value, second_speed_value, 0),
        )
        self.motor._set_property.assert_called_once_with(
            *expected_speed_params
        )

        self.assertEqual(
            mock.call(self.motor.PropertyType.FIRST_SPEED),
            self.motor._get_property.call_args_list[0],
        )
        self.assertEqual(
            mock.call(self.motor.PropertyType.SECOND_SPEED),
            self.motor._get_property.call_args_list[1],
        )

    def test_set_speed_with_none(self):
        """Test set_speed method with none input."""
        self.motor.set_speed()

        self.assertEqual(
            mock.call(self.motor.PropertyType.FIRST_SPEED),
            self.motor._get_property.call_args_list[0],
        )
        self.assertEqual(
            mock.call(self.motor.PropertyType.SECOND_SPEED),
            self.motor._get_property.call_args_list[1],
        )

    def test_set_degree(self):
        """Test set_degree method."""
        expected_values = first_degree_value, second_degree_value = 50, 50
        self.motor.set_degree(*expected_values)

        expected_degree_params = (
            self.mock_kwargs["id_"],
            self.motor.ControlType.DEGREE.value,
            (first_degree_value, second_degree_value, 0),
        )
        self.motor._set_property.assert_called_once_with(
            *expected_degree_params)

        self.assertEqual(
            mock.call(self.motor.PropertyType.FIRST_DEGREE),
            self.motor._get_property.call_args_list[0],
        )
        self.assertEqual(
            mock.call(self.motor.PropertyType.SECOND_DEGREE),
            self.motor._get_property.call_args_list[1],
        )

    def test_set_degree_with_none(self):
        """Test set_degree method with none input."""
        self.motor.set_degree()

        self.assertEqual(
            mock.call(self.motor.PropertyType.FIRST_DEGREE),
            self.motor._get_property.call_args_list[0],
        )
        self.assertEqual(
            mock.call(self.motor.PropertyType.SECOND_DEGREE),
            self.motor._get_property.call_args_list[1],
        )


if __name__ == "__main__":
    unittest.main()
