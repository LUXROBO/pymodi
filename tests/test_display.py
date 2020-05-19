import unittest

from unittest import mock

from modi.module.output_module.display import Display


class TestDisplay(unittest.TestCase):
    """Tests for 'Display' class."""

    def setUp(self):
        """Set up test fixtures, if any."""
        self.mock_kwargs = {"id_": -1, "uuid": -1, "msg_send_q": None}
        self.display = Display(**self.mock_kwargs)

        def eval_set_property(id, property_type, data, property_data_type):
            eval_result = {
                self.display.PropertyType.TEXT.value: [property_type],
                self.display.PropertyType.VARIABLE.value: property_type,
                self.display.PropertyType.CLEAR.value: property_type,
            }.get(property_type)
            return eval_result

        self.display._set_property = mock.Mock(side_effect=eval_set_property)
        self.display._msg_send_q = mock.Mock()

    def tearDown(self):
        """Tear down test fixtures, if any."""
        del self.display

    def test_set_text(self):
        """Test set_text method."""
        mock_text = "abcd"
        self.display.set_text(text=mock_text)

        expected_clear_params = (
            self.mock_kwargs["id_"],
            self.display.PropertyType.CLEAR.value,
            bytes(2),
            self.display.PropertyDataType.RAW,
        )

        expected_text_params = (
           self.mock_kwargs["id_"],
           self.display.PropertyType.TEXT.value,
           mock_text,
           self.display.PropertyDataType.STRING,
        )

        self.assertEqual(self.display._set_property.call_count, 2)

        # TODO: Refactor two functions calls below to use assert_has_calls()
        self.assertEqual(
           mock.call(*expected_clear_params),
           self.display._set_property.call_args_list[0],
        )
        self.assertEqual(
           mock.call(*expected_text_params),
           self.display._set_property.call_args_list[1],
        )

    def test_set_variable(self):
        """Test set_variable method."""
        mock_variable = "12345"
        mock_position = 5
        self.display.set_variable(mock_variable, mock_position, mock_position)

        expected_clear_params = (
            self.mock_kwargs["id_"],
            self.display.PropertyType.CLEAR.value,
            bytes(2),
            self.display.PropertyDataType.RAW,
        )

        expected_variable_params = (
            self.mock_kwargs["id_"],
            self.display.PropertyType.VARIABLE.value,
            (mock_variable, mock_position, mock_position),
            self.display.PropertyDataType.DISPLAY_VAR,
        )

        self.assertEqual(self.display._set_property.call_count, 2)

        # TODO: Refactor two functions calls below to use assert_has_calls()
        self.assertEqual(
            mock.call(*expected_clear_params),
            self.display._set_property.call_args_list[0],
        )
        self.assertEqual(
            mock.call(*expected_variable_params),
            self.display._set_property.call_args_list[1],
        )

    def test_clear(self):
        """Test clear method."""
        self.display.clear()

        # Check if set_property is called once with the specified arguments
        expected_clear_params = (
            self.mock_kwargs["id_"],
            self.display.PropertyType.CLEAR.value,
            bytes(2),
            self.display.PropertyDataType.RAW,
        )
        self.display._set_property.assert_called_once_with(
            *expected_clear_params)

        # Check if correct message has been passed to serial_write_q
        self.display._msg_send_q.put.assert_called_once_with(
            self.display.PropertyType.CLEAR.value
        )


if __name__ == "__main__":
    unittest.main()
