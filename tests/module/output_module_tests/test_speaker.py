import unittest

from unittest import mock

from modi.module.output_module.speaker import Speaker


class TestSpeaker(unittest.TestCase):
    """Tests for 'Speaker' class."""

    def setUp(self):
        """Set up test fixtures, if any."""
        self.mock_kwargs = {"id_": -1, "uuid": -1, "msg_send_q": None}
        self.speaker = Speaker(**self.mock_kwargs)

        def eval_set_property(id, command_type, data, property_data_type):
            return command_type

        self.speaker._set_property = mock.Mock(side_effect=eval_set_property)
        self.speaker._get_property = mock.Mock(return_value=0)
        self.speaker._msg_send_q = mock.Mock()

    def tearDown(self):
        """Tear down test fixtures, if any."""
        del self.speaker

    def test_set_tune(self):
        """Test set_tune method."""
        expected_values = frequency, volume = (
            self.speaker.Scale.F_RA_6.value, 30
        )
        self.speaker.tune = expected_values

        expected_tune_params = (
            self.mock_kwargs["id_"],
            self.speaker.CommandType.SET_TUNE,
            expected_values,
            self.speaker.PropertyDataType.FLOAT,
        )

        self.assertEqual(self.speaker._msg_send_q.put.call_count, 2)
        self.speaker._set_property.assert_called_once_with(
            *expected_tune_params)

    def test_get_tune(self):
        """Test get_tune method with none input."""
        _ = self.speaker.tune
        self.assertEqual(self.speaker._get_property.call_count, 2)

    def test_set_frequency(self):
        """Test set_frequency method."""
        expeceted_frequency = 50
        setter_mock = mock.Mock(wraps=Speaker.tune.fset)
        mock_property = Speaker.tune.setter(setter_mock)
        with mock.patch.object(Speaker, 'tune', mock_property):
            self.speaker.frequency = expeceted_frequency
            setter_mock.assert_called_once_with(self.speaker,
                                                (expeceted_frequency, 0))

    def test_get_frequency(self):
        """Test get_frequency method with none input."""
        _ = self.speaker.frequency
        self.speaker._get_property.assert_called_once_with(
            self.speaker.PropertyType.FREQUENCY
        )

    def test_set_volume(self):
        """Test set_volume method."""
        expeceted_volume = 50
        setter_mock = mock.Mock(wraps=Speaker.tune.fset)
        mock_property = Speaker.tune.setter(setter_mock)
        with mock.patch.object(Speaker, 'tune', mock_property):
            self.speaker.volume = expeceted_volume
            setter_mock.assert_called_once_with(self.speaker,
                                                (0, expeceted_volume))

    def test_get_volume(self):
        """Test get_volume method with none input."""
        _ = self.speaker.volume
        self.speaker._get_property.assert_called_once_with(
            self.speaker.PropertyType.VOLUME
        )

    def test_set_off(self):
        """Test set_off method"""
        expeceted_values = frequency, volume = 0, 0
        setter_mock = mock.Mock(wraps=Speaker.tune.fset)
        mock_property = Speaker.tune.setter(setter_mock)
        with mock.patch.object(Speaker, 'tune', mock_property):
            self.speaker.turn_off()
            setter_mock.assert_called_once_with(self.speaker,
                                                expeceted_values)


if __name__ == "__main__":
    unittest.main()
