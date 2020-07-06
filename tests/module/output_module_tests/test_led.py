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
        sent_messages = []
        while not self.send_q.empty():
            sent_messages.append(self.send_q.get_nowait())
        self.assertTrue(Led.request_property(
            -1, Led.PropertyType.RED) in sent_messages)
        self.assertTrue(Led.request_property(
            -1, Led.PropertyType.GREEN) in sent_messages)
        self.assertTrue(Led.request_property(
            -1, Led.PropertyType.BLUE) in sent_messages)
        self.assertTrue(set_message in sent_messages)

    def test_on(self):
        """Test on method."""
        expected_color = (255, 255, 255)
        self.led.rgb = expected_color
        set_message = parse_message(0x04, 16, -1, parse_data(
            expected_color, 'int'))
        sent_messages = []
        while not self.send_q.empty():
            sent_messages.append(self.send_q.get_nowait())
        self.assertTrue(Led.request_property(
            -1, Led.PropertyType.RED) in sent_messages)
        self.assertTrue(Led.request_property(
            -1, Led.PropertyType.GREEN) in sent_messages)
        self.assertTrue(Led.request_property(
            -1, Led.PropertyType.BLUE) in sent_messages)
        self.assertTrue(set_message in sent_messages)

    def test_off(self):
        """Test off method."""
        expected_color = (0, 0, 0)
        self.led.rgb = expected_color
        set_message = parse_message(0x04, 16, -1, parse_data(
            expected_color, 'int'))
        sent_messages = []
        while not self.send_q.empty():
            sent_messages.append(self.send_q.get_nowait())
        self.assertTrue(Led.request_property(
            -1, Led.PropertyType.RED) in sent_messages)
        self.assertTrue(Led.request_property(
            -1, Led.PropertyType.GREEN) in sent_messages)
        self.assertTrue(Led.request_property(
            -1, Led.PropertyType.BLUE) in sent_messages)
        self.assertTrue(set_message in sent_messages)

    def test_set_red(self):
        """Test set_red method."""
        expected_color = (20, 0, 0)
        set_message = parse_message(0x04, 16, -1, parse_data(
            expected_color, 'int'))
        sent_messages = []
        self.led.red = 20
        while not self.send_q.empty():
            sent_messages.append(self.send_q.get_nowait())
        self.assertTrue(Led.request_property(
            -1, Led.PropertyType.RED) in sent_messages)
        self.assertTrue(Led.request_property(
            -1, Led.PropertyType.GREEN) in sent_messages)
        self.assertTrue(Led.request_property(
            -1, Led.PropertyType.BLUE) in sent_messages)
        self.assertTrue(set_message in sent_messages)

    def test_get_red(self):
        """Test get_red method with none input."""
        _ = self.led.red
        self.assertEqual(
            self.send_q.get(),
            Led.request_property(-1, Led.PropertyType.RED))

    def test_set_green(self):
        """Test set_green method."""
        expected_color = (0, 20, 0)
        set_message = parse_message(0x04, 16, -1, parse_data(
            expected_color, 'int'))
        sent_messages = []
        self.led.green = 20
        while not self.send_q.empty():
            sent_messages.append(self.send_q.get_nowait())
        self.assertTrue(Led.request_property(
            -1, Led.PropertyType.RED) in sent_messages)
        self.assertTrue(Led.request_property(
            -1, Led.PropertyType.GREEN) in sent_messages)
        self.assertTrue(Led.request_property(
            -1, Led.PropertyType.BLUE) in sent_messages)
        self.assertTrue(set_message in sent_messages)

    def test_get_green(self):
        """Test set_green method with none input."""
        _ = self.led.green
        self.assertEqual(
            self.send_q.get(),
            Led.request_property(-1, Led.PropertyType.GREEN))

    def test_set_blue(self):
        """Test blue method."""
        expected_color = (0, 0, 20)
        set_message = parse_message(0x04, 16, -1, parse_data(
            expected_color, 'int'))
        sent_messages = []
        self.led.blue = 20
        while not self.send_q.empty():
            sent_messages.append(self.send_q.get_nowait())
        self.assertTrue(Led.request_property(
            -1, Led.PropertyType.RED) in sent_messages)
        self.assertTrue(Led.request_property(
            -1, Led.PropertyType.GREEN) in sent_messages)
        self.assertTrue(Led.request_property(
            -1, Led.PropertyType.BLUE) in sent_messages)
        self.assertTrue(set_message in sent_messages)

    def test_get_blue(self):
        """Test get blue method with none input."""
        _ = self.led.blue
        self.assertEqual(
            self.send_q.get(),
            Led.request_property(-1, Led.PropertyType.BLUE))


if __name__ == "__main__":
    unittest.main()
