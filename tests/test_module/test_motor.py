#!/usr/bin/env python
# -*- coding: utf-8 -*-

import mock
import unittest

from modi.module.output_module.motor import Motor


class TestMotor(unittest.TestCase):
    """Tests for 'Motor' class."""

    def setUp(self):
        """Set up test fixtures, if any."""
        self.mock_kwargs = {
            "module_id": -1,
            "module_uuid": -1,
            "modi": None,
            "serial_write_q": None,
        }
        self.motor = Motor(**self.mock_kwargs)

        def eval_set_property(id, command_type, data):
            return command_type

        self.motor._set_property = mock.Mock(side_effect=eval_set_property)
        self.motor._get_property = mock.Mock()
        self.motor._serial_write_q = mock.Mock()

    def tearDown(self):
        """Tear down test fixtures, if any."""
        del self.motor

    # def test_set_torque(self):
    #    """Test set_torque method."""
    #    expected_values = first_torque_value, second_torque_value = 50, 50
    #    self.motor.set_torque(*expected_values)

    #    expected_torque_params = (
    #        self.mock_kwargs["module_id"],
    #        self.motor.ControlType.TORQUE,
    #        (*expected_values, 0),
    #    )
    #    self.motor._set_property.assert_called_once_with(*expected_torque_params)

    #    self.assertEqual(
    #        mock.call(self.motor.PropertyType.FIRST_TORQUE),
    #        self.motor._get_property.call_args_list[0],
    #    )
    #    self.assertEqual(
    #        mock.call(self.motor.PropertyType.SECOND_TORQUE),
    #        self.motor._get_property.call_args_list[1],
    #    )

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
            self.mock_kwargs["module_id"],
            self.motor.ControlType.SPEED,
            (*expected_values, 0),
        )
        self.motor._set_property.assert_called_once_with(*expected_speed_params)

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
            self.mock_kwargs["module_id"],
            self.motor.ControlType.DEGREE,
            (*expected_values, 0),
        )
        self.motor._set_property.assert_called_once_with(*expected_degree_params)

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
