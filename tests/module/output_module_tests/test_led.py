import unittest

from modi.module.output_module.led import Led
from queue import Queue
from modi.util.msgutil import parse_data, parse_message


class TestLed(unittest.TestCase):
    """Tests for 'Led' class."""

    def setUp(self):
        """Set up test fixtures, if any."""
        self.send_q = Queue()
        self.mock_kwargs = {"id_": -1, "uuid": -1, "msg_send_q": self.send_q}
        self.led = Led(**self.mock_kwargs)

    def tearDown(self):
        """Tear down test fixtures, if any."""
        del self.led

    def test_set_rgb(self):
        """Test set_rgb method with user-defined inputs."""
        expected_color = (10, 100, 200)
        self.led.rgb = expected_color
        set_message = parse_message(0x04, 16, -1, parse_data(
            expected_color, 'int'))
        self.assertEqual(
            self.send_q.get(),
            set_message
        )

    def test_on(self):
        """Test on method."""
        expected_color = (255, 255, 255)
        self.led.rgb = expected_color
        set_message = parse_message(0x04, 16, -1, parse_data(
            expected_color, 'int'))
        self.assertEqual(
            self.send_q.get(),
            set_message
        )

    def test_off(self):
        """Test off method."""
        expected_color = (0, 0, 0)
        self.led.rgb = expected_color
        set_message = parse_message(0x04, 16, -1, parse_data(
            expected_color, 'int'))
        self.assertEqual(
            self.send_q.get(),
            set_message
        )

    def test_set_red(self):
        """Test set_red method."""
        expected_color = (20, 0, 0)
        self.led.red = 20
        set_message = parse_message(0x04, 16, -1, parse_data(
            expected_color, 'int'))
        print(self.send_q.get())
        print(self.send_q.get())
        print(self.send_q.get())
        print(self.send_q.get())
        print(self.send_q.get())
        print(self.send_q.get())
        print(set_message)
        # self.assertEqual(
        #     self.send_q.get(),
        #     Led.request_property(-1, Led.PropertyType.GREEN)
        # )
        # self.assertEqual(
        #     self.send_q.get(),
        #     Led.request_property(-1, Led.PropertyType.BLUE)
        # )
        # self.assertEqual(
        #     self.send_q.get(),
        #     set_message
        # )

    # def test_get_red(self):
    #     """Test get_red method with none input."""
    #     _ = self.led.red
    #     self.led._get_property.assert_called_once_with(
    #         self.led.PropertyType.RED)

    # def test_set_green(self):
    #     """Test set_green method."""
    #     expected_color = 20
    #     setter_mock = mock.Mock(wraps=Led.rgb.fset)
    #     mock_property = Led.rgb.setter(setter_mock)
    #     with mock.patch.object(Led, 'rgb', mock_property):
    #         self.led.green = expected_color
    #         setter_mock.assert_called_once_with(self.led,
    #                                             (0, expected_color, 0))
    #
    # def test_get_green(self):
    #     """Test set_green method with none input."""
    #     _ = self.led.green
    #     self.led._get_property.assert_called_once_with(
    #         self.led.PropertyType.GREEN)
    #
    # def test_set_blue(self):
    #     """Test blue method."""
    #     expected_color = 20
    #     setter_mock = mock.Mock(wraps=Led.rgb.fset)
    #     mock_property = Led.rgb.setter(setter_mock)
    #     with mock.patch.object(Led, 'rgb', mock_property):
    #         self.led.blue = expected_color
    #         setter_mock.assert_called_once_with(self.led,
    #                                             (0, 0, expected_color))
    #
    # def test_get_blue(self):
    #     """Test get blue method with none input."""
    #     _ = self.led.blue
    #     self.led._get_property.assert_called_once_with(
    #         self.led.PropertyType.BLUE)


if __name__ == "__main__":
    unittest.main()
