import setproctitle

import multiprocessing as mp
import threading

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

        can_read_thread = threading.Thread(target=self.__can_task.run_read,args=(self.stopped(),))
        can_read_thread.daemon = True
        can_read_thread.start()

        can_write_thread = threading.Thread(target=self.__can_task.run_write,args=(self.stopped(),))
        can_write_thread.daemon = True
        can_write_thread.start()

        can_read_thread.join()
        can_write_thread.join()

        print('finish can process')

    def stop(self):
        """ Stop serial task
        """
        print('process stop : ',self.__stop)
        self.__stop.set()

    def stopped(self):
        """ Check serial task status
        """

        return self.__stop.is_set()
