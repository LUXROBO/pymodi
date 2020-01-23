import threading

from modi._executor_task import ExecutorTask


class ExecutorThread(threading.Thread):
    def __init__(self, serial_write_q, json_recv_q, module_ids, modules):
        super(ExecutorThread, self).__init__()
        self.__exe_task = ExecutorTask(serial_write_q, json_recv_q, module_ids, modules)
        self.__stop = threading.Event()

    def run(self):
        self.__exe_task.init_modules()
        while not self.stopped():
            self.__exe_task.start_thread()

    def stop(self):
        self.__stop.set()

    def stopped(self):
        return self.__stop.is_set()
