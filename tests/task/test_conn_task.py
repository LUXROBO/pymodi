import unittest
# from unittest import mock

from modi.task.conn_task import ConnTask


class TestConnTask(unittest.TestCase):
    """Tests for 'ConnTask' class"""

    def setUp(self):
        """Set up test fixtures, if any."""
        self.mock_kwargs = {"ser_recv_q": None, "ser_send_q": None}
        self.conn_task = ConnTask(**self.mock_kwargs)

    def tearDown(self):
        """Tear down test fixtures, if any."""
        del self.conn_task


if __name__ == "__main__":
    unittest.main()
