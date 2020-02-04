import unittest

from unittest import mock

from modi.modi import MODI


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
        self.assertListEqual(self.modi._modules, list())
        self.assertDictEqual(self.modi._module_ids, dict())

    def test_exit(self):
        self.modi.exit()

        self.modi._ser_proc.stop.assert_called_once_with()
        self.modi._par_proc.stop.assert_called_once_with()
        self.modi._exe_thrd.stop.assert_called_once_with()


if __name__ == "__main__":
    unittest.main()
