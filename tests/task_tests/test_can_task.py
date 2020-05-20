import unittest
from unittest import mock

from modi.task.can_task import CanTask


class TestCanTask(unittest.TestCase):
    """Tests for 'CanTask' class"""

    def setUp(self):
        """Set up test fixtures, if any."""
        self.mock_kwargs = {"can_recv_q": None, "can_send_q": None}
        self.canTask = CanTask(**self.mock_kwargs)

    def tearDown(self):
        """Tear down test fixtures, if any."""
        del self.canTask

    # def test_open_conn(self):
    #     """Test open_conn method"""
    #     self.canTask.open_conn()


if __name__ == "__main__":
    unittest.main()
