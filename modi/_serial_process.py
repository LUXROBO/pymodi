import threading
import setproctitle

import multiprocessing as mp

from modi._serial_task import SerialTask


class SerialProcess(mp.Process):
    """
    :param queue serial_read_q: Multiprocessing Queue for serial reading data
    :param queue serial_write_q: Multiprocessing Queue for serial writing data
    """

    def __init__(self, serial_read_q, serial_write_q):
        super().__init__()
        self.__ser_task = SerialTask(serial_read_q, serial_write_q)
        self.__stop = mp.Event()

        setproctitle.setproctitle('pymodi-serial')

        self.__delay = 0.001

    def run(self):
        """ Run serial task
        """

        read_thread = threading.Thread(
            target=self.__ser_task.run_read_serial, args=(self.__delay,))
        read_thread.daemon = True
        read_thread.start()

        write_thread = threading.Thread(
            target=self.__ser_task.run_write_serial, args=(self.__delay,))
        write_thread.daemon = True
        write_thread.start()

        read_thread.join()
        write_thread.join()

    def stop(self):
        """ Stop serial task
        """

        self.__stop.set()

    def stopped(self):
        """ Check serial task status
        """

        return self.__stop.is_set()
