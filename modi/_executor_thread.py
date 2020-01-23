import threading

from modi._executor_task import ExecutorTask


class ExecutorThread(threading.Thread):
    """
    :param queue serial_write_q: Multiprocessing Queue for serial writing message
    :param queue json_recv_q: Multiprocessing Queue for json message
    :param dict() module_ids: dict() of key: module_id, value: ['timestamp', 'uuid']
    :param list() modules: list() of module instance
    """

    def __init__(self, serial_write_q, json_recv_q, module_ids, modules):
        super(ExecutorThread, self).__init__()
        self.__exe_task = ExecutorTask(serial_write_q, json_recv_q, module_ids, modules)
        self.__stop = threading.Event()

    def run(self):
        """ Run executor task
        """

        self.__exe_task.init_modules()
        while not self.stopped():
            self.__exe_task.run()

    def stop(self):
        """ Stop executor task
        """

        self.__stop.set()

    def stopped(self):
        """ Check executor task status
        """

        return self.__stop.is_set()
