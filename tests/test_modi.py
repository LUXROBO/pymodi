import unittest

from unittest import mock

from modi.modi import MODI

from modi.module.setup_module.setup_module import SetupModule
from modi.module.input_module.input_module import InputModule
from modi.module.output_module.output_module import OutputModule


class TestModi(unittest.TestCase):
    """Tests for 'modi' class."""

    def setUp(self):
        """Set up test fixtures, if any."""
        self.modi = MODI(test=True)

        self.modi._ser_proc = mock.Mock()
        self.modi._par_proc = mock.Mock()
        self.modi._exe_thrd = mock.Mock()

    def tearDown(self):
        """Tear down test fixtures, if any."""
        del self.modi

    def test_init(self):
        """Test correct initialization of modi instance."""
        self.assertListEqual(self.modi._modules, list())
        self.assertDictEqual(self.modi._module_ids, dict())

    def test_exit(self):
        """Test exit method."""
        self.modi.exit()

        self.modi._ser_proc.stop.assert_called_once_with()
        self.modi._par_proc.stop.assert_called_once_with()
        self.modi._exe_thrd.stop.assert_called_once_with()

    def test_get_modules(self):
        mock_input_values = (-1, -1, None)
        self.modi._modules = [
            SetupModule(*mock_input_values),
            InputModule(*mock_input_values),
            OutputModule(*mock_input_values),
        ]

        self.assertIsInstance(self.modi.modules, tuple)
        self.assertTupleEqual(self.modi.modules, tuple(self.modi._modules))


if __name__ == "__main__":
    unittest.main()
