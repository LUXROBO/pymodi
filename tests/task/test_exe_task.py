import unittest
# from unittest import mock

from modi.task.exe_task import ExeTask


class TestExeTask(unittest.TestCase):
    """Tests for 'ExeTask' class"""

    def setUp(self):
        """Set up test fixtures, if any."""
        self.mock_kwargs = {"ser_recv_q": None, "ser_send_q": None}
        self.exe_task = ExeTask(**self.mock_kwargs)

    def tearDown(self):
        """Tear down test fixtures, if any."""
        del self.exe_task


if __name__ == "__main__":
    unittest.main()
