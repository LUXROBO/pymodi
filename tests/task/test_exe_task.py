import unittest

from modi.util.miscellaneous import MockConn
from modi.task.exe_task import ExeTask


class TestExeTask(unittest.TestCase):
    """Tests for 'ExeTask' class"""

    def setUp(self):
        """Set up test fixtures, if any."""
        self.topology_data = dict()
        self.conn = MockConn()
        self.mock_kwargs = {"topology_data": self.topology_data,
                            "modules": [],
                            "conn_task": self.conn,
                            }
        self.exe_task = ExeTask(**self.mock_kwargs)

    def tearDown(self):
        """Tear down test fixtures, if any."""
        del self.exe_task


if __name__ == "__main__":
    unittest.main()
