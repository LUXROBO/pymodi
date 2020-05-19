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
        self.speaker._get_property = mock.Mock()
        self.speaker._msg_send_q = mock.Mock()

    def tearDown(self):
        """Tear down test fixtures, if any."""
        del self.speaker

    @mock.patch.object(Speaker, "set_volume")
    @mock.patch.object(Speaker, "set_frequency")
    def test_set_tune(self, mock_set_frequency, mock_set_volume):
        """Test set_tune method."""
        expected_values = frequency, volume = (
            self.speaker.Scale.F_RA_6.value, 30
        )
        self.speaker.set_tune(*expected_values)

        expected_tune_params = (
            self.mock_kwargs["id_"],
            self.speaker.CommandType.SET_TUNE.value,
            expected_values,
            self.speaker.PropertyDataType.FLOAT,
        )
        self.speaker._set_property.assert_called_once_with(
            *expected_tune_params)
        self.speaker._msg_send_q.put.assert_called_once_with(
            self.speaker.CommandType.SET_TUNE.value
        )

        mock_set_frequency.assert_called_once_with()
        mock_set_volume.assert_called_once_with()

    @mock.patch.object(Speaker, "set_volume")
    @mock.patch.object(Speaker, "set_frequency")
    def test_set_tune_with_none(self, mock_set_frequency, mock_set_volume):
        """Test set_tune method with none input."""
        self.speaker.set_tune()

        mock_set_frequency.assert_called_once_with()
        mock_set_volume.assert_called_once_with()

    @mock.patch.object(Speaker, "set_tune")
    def test_set_frequency(self, mock_set_tune):
        """Test set_frequency method."""
        expeceted_frequency = 50
        self.speaker.set_frequency(frequency_value=expeceted_frequency)
        mock_set_tune.assert_called_once_with(
            frequency_value=expeceted_frequency)

    def test_set_frequency_with_none(self):
        """Test set_frequency method with none input."""
        self.speaker.set_frequency(frequency_value=None)
        self.speaker._get_property.assert_called_once_with(
            self.speaker.PropertyType.FREQUENCY
        )

    @mock.patch.object(Speaker, "set_tune")
    def test_set_volume(self, mock_set_tune):
        """Test set_volume method."""
        expeceted_volume = 50
        self.speaker.set_volume(volume_value=expeceted_volume)
        mock_set_tune.assert_called_once_with(volume_value=expeceted_volume)

    def test_set_volume_with_none(self):
        """Test set_volume method with none input."""
        self.speaker.set_volume(volume_value=None)
        self.speaker._get_property.assert_called_once_with(
            self.speaker.PropertyType.VOLUME
        )

    @mock.patch.object(Speaker, "set_tune")
    def test_set_off(self, mock_set_tune):
        """Test set_off method"""
        self.speaker.set_off()

        expeceted_values = frequency, volume = 0, 0
        mock_set_tune.assert_called_once_with(*expeceted_values)


if __name__ == "__main__":
    unittest.main()
