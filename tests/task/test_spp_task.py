import unittest
from unittest import mock

from modi.task.spp_task import SppTask


class TestSppTask(unittest.TestCase):
    """Tests for 'SppTask' class"""

    def setUp(self):
        """Set up test fixtures, if any."""
        self.mock_kwargs = {"ser_recv_q": None, "ser_send_q": None}
        self.spp_task = SppTask(**self.mock_kwargs)

    def tearDown(self):
        """Tear down test fixtures, if any."""
        del self.spp_task


if __name__ == "__main__":
    unittest.main()
