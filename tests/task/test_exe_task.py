import unittest

from queue import Queue
from modi.task.exe_task import ExeTask


class TestExeTask(unittest.TestCase):
    """Tests for 'ExeTask' class"""

    def setUp(self):
        """Set up test fixtures, if any."""
        self.send_q = Queue()
        self.recv_q = Queue()
        self.topology_data = dict()
        self.mock_kwargs = {"recv_q": self.recv_q,
                            "send_q": self.send_q,
                            "topology_data": self.topology_data,
                            "modules": [],
                            "module_ids": None,
                            "init_event": None,
                            "nb_modules": 1,
                            "firmware_updater": None}
        self.exe_task = ExeTask(**self.mock_kwargs)

    def tearDown(self):
        """Tear down test fixtures, if any."""
        del self.exe_task

    def test_request_topology(self):
        topology_message = '{"c":7,"s":-1,"d":0,"b":"AAAAAAAAAAA=","l":8}'
        self.recv_q.put(topology_message)
        self.exe_task.run(0.1)
        self.assertEqual(len(self.topology_data), 1)
        self.assertTrue(-1 in self.topology_data)


if __name__ == "__main__":
    unittest.main()
