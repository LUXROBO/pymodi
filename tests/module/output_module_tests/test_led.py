import unittest

from unittest import mock

from modi.module.output_module.led import Led


class TestLed(unittest.TestCase):
    """Tests for 'Led' class."""

    def setUp(self):
        """Set up test fixtures, if any."""
        self.mock_kwargs = {"id_": -1, "uuid": -1, "msg_send_q": None}
        self.led = Led(**self.mock_kwargs)

        def eval_set_property(id, command_type, data):
            return command_type

        self.led._set_property = mock.Mock(side_effect=eval_set_property)
        self.led._get_property = mock.Mock(return_value=0)
        self.led._msg_send_q = mock.Mock()

    def tearDown(self):
        """Tear down test fixtures, if any."""
        del self.led

    def test_set_rgb(self):
        """Test set_rgb method with user-defined inputs."""
        expected_color = (10, 100, 200)
        self.led.rgb = expected_color

        expected_rgb_params = (
            self.mock_kwargs["id_"],
            self.led.CommandType.SET_RGB,
            expected_color,
        )
        self.led._set_property.assert_called_once_with(*expected_rgb_params)
        self.assertEqual(self.led._msg_send_q.put.call_count, 3)

    def test_on(self):
        """Test on method."""
        expected_color = (255, 255, 255)
        setter_mock = mock.Mock(wraps=Led.rgb.fset)
        mock_property = Led.rgb.setter(setter_mock)
        with mock.patch.object(Led, 'rgb', mock_property):
            self.led.turn_on()
            setter_mock.assert_called_once_with(self.led, expected_color)

    def test_off(self):
        """Test off method."""
        expected_color = (0, 0, 0)
        setter_mock = mock.Mock(wraps=Led.rgb.fset)
        mock_property = Led.rgb.setter(setter_mock)
        with mock.patch.object(Led, 'rgb', mock_property):
            self.led.turn_off()
            setter_mock.assert_called_once_with(self.led, expected_color)

    def test_set_red(self):
        """Test set_red method."""
        expected_color = 20
        setter_mock = mock.Mock(wraps=Led.rgb.fset)
        mock_property = Led.rgb.setter(setter_mock)
        with mock.patch.object(Led, 'rgb', mock_property):
            self.led.red = expected_color
            setter_mock.assert_called_once_with(self.led,
                                                (expected_color, None, None))

    def test_get_red(self):
        """Test get_red method with none input."""
        _ = self.led.red
        self.led._get_property.assert_called_once_with(
            self.led.PropertyType.RED)

    def test_set_green(self):
        """Test set_green method."""
        expected_color = 20
        setter_mock = mock.Mock(wraps=Led.rgb.fset)
        mock_property = Led.rgb.setter(setter_mock)
        with mock.patch.object(Led, 'rgb', mock_property):
            self.led.green = expected_color
            setter_mock.assert_called_once_with(self.led,
                                                (None, expected_color, None))

    def test_get_green(self):
        """Test set_green method with none input."""
        _ = self.led.green
        self.led._get_property.assert_called_once_with(
            self.led.PropertyType.GREEN)

    def test_set_blue(self):
        """Test blue method."""
        expected_color = 20
        setter_mock = mock.Mock(wraps=Led.rgb.fset)
        mock_property = Led.rgb.setter(setter_mock)
        with mock.patch.object(Led, 'rgb', mock_property):
            self.led.blue = expected_color
            setter_mock.assert_called_once_with(self.led,
                                                (None, None, expected_color))

    def test_get_blue(self):
        """Test get blue method with none input."""
        _ = self.led.blue
        self.led._get_property.assert_called_once_with(
            self.led.PropertyType.BLUE)


if __name__ == "__main__":
    unittest.main()
