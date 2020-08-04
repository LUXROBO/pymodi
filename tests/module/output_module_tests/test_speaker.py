import unittest

from queue import Queue
from modi.module.output_module.speaker import Speaker
from modi.util.msgutil import parse_data, parse_message


class TestSpeaker(unittest.TestCase):
    """Tests for 'Speaker' class."""

    def setUp(self):
        """Set up test fixtures, if any."""
        self.send_q = Queue()
        self.mock_kwargs = {"id_": -1, "uuid": -1, "msg_send_q": self.send_q}
        self.speaker = Speaker(**self.mock_kwargs)

    def tearDown(self):
        """Tear down test fixtures, if any."""
        del self.speaker

    def test_set_tune(self):
        """Test set_tune method."""
        expected_values = frequency, volume = (
            self.speaker.Scale.F_LA_6.value, 30
        )
        self.speaker.tune = expected_values
        sent_messages = []
        while not self.send_q.empty():
            sent_messages.append(self.send_q.get_nowait())
        self.assertTrue(
            Speaker.request_property(
                -1, Speaker.PropertyType.FREQUENCY) in sent_messages)
        self.assertTrue(
            Speaker.request_property(
                -1, Speaker.PropertyType.VOLUME) in sent_messages)
        self.assertTrue(
            parse_message(
                0x04, 16, -1, parse_data(
                    expected_values, 'float')) in sent_messages)

    def test_get_tune(self):
        """Test get_tune method with none input."""
        _ = self.speaker.tune
        sent_messages = []
        while not self.send_q.empty():
            sent_messages.append(self.send_q.get_nowait())
        self.assertTrue(
            Speaker.request_property(
                -1, Speaker.PropertyType.FREQUENCY) in sent_messages)
        self.assertTrue(
            Speaker.request_property(
                -1, Speaker.PropertyType.VOLUME) in sent_messages)

    def test_set_frequency(self):
        """Test set_frequency method."""
        expecetd_frequency = 50
        self.speaker.frequency = expecetd_frequency
        expected_values = (50, 0)
        sent_messages = []
        while not self.send_q.empty():
            sent_messages.append(self.send_q.get_nowait())
        self.assertTrue(
            Speaker.request_property(
                -1, Speaker.PropertyType.FREQUENCY) in sent_messages)
        self.assertTrue(
            Speaker.request_property(
                -1, Speaker.PropertyType.VOLUME) in sent_messages)
        self.assertTrue(
            parse_message(
                0x04, 16, -1, parse_data(
                    expected_values, 'float')) in sent_messages)

    def test_get_frequency(self):
        """Test get_frequency method with none input."""
        _ = self.speaker.frequency
        self.assertEqual(
            self.send_q.get(),
            Speaker.request_property(-1, Speaker.PropertyType.FREQUENCY))

    def test_set_volume(self):
        """Test set_volume method."""
        expected_volume = 50
        expected_values = (0, 50)
        self.speaker.volume = expected_volume
        sent_messages = []
        while not self.send_q.empty():
            sent_messages.append(self.send_q.get_nowait())
        self.assertTrue(
            Speaker.request_property(
                -1, Speaker.PropertyType.FREQUENCY) in sent_messages)
        self.assertTrue(
            Speaker.request_property(
                -1, Speaker.PropertyType.VOLUME) in sent_messages)
        self.assertTrue(
            parse_message(
                0x04, 16, -1, parse_data(
                    expected_values, 'float')) in sent_messages)

    def test_get_volume(self):
        """Test get_volume method with none input."""
        _ = self.speaker.volume
        self.assertEqual(
            self.send_q.get(),
            Speaker.request_property(-1, Speaker.PropertyType.VOLUME))

    def test_set_off(self):
        """Test set_off method"""
        expected_values = (0, 0)
        self.speaker.tune = expected_values
        sent_messages = []
        while not self.send_q.empty():
            sent_messages.append(self.send_q.get_nowait())
        self.assertTrue(
            Speaker.request_property(
                -1, Speaker.PropertyType.FREQUENCY) in sent_messages)
        self.assertTrue(
            Speaker.request_property(
                -1, Speaker.PropertyType.VOLUME) in sent_messages)
        self.assertTrue(
            parse_message(
                0x04, 16, -1, parse_data(
                    expected_values, 'float')) in sent_messages)


if __name__ == "__main__":
    unittest.main()
