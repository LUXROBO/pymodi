import setproctitle

import multiprocessing as mp

from modi._can_task import CanTask


class CanProcess(mp.Process):
    """
    :param queue serial_read_q: Multiprocessing Queue for serial reading data
    :param queue serial_write_q: Multiprocessing Queue for serial writing data
    """

    def __init__(self, can_read_q, can_write_q):
        super(CanProcess, self).__init__()
        self.__can_task = CanTask(can_read_q, can_write_q)
        self.__stop = mp.Event()

        setproctitle.setproctitle('pymodi-serial')

    def run(self):
        """ Run serial task
        """

        while not self.stopped():
            self.__can_task.run()

    def stop(self):
        """ Stop serial task
        """

        self.__stop.set()

    def stopped(self):
        """ Check serial task status
        """

        return self.__stop.is_set()
