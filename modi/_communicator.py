
import threading as th
import multiprocessing as mp

from modi._communicator_task import CommunicatorTask
from modi._ser_task import SerTask
from modi._can_task import CanTask


class Communicator(mp.Process):
    """
    :param queue read_q: Multiprocessing Queue for reading raw data
    :param queue write_q: Multiprocessing Queue for writing raw data
    """

    def __init__(self, read_q, write_q):
        super().__init__()
        self.__task = CanTask(read_q, write_q) if self.__is_modi_pi() else SerTask(read_q, write_q)
        self.__delay = 0.001

    def __is_modi_pi(self):
        return CommunicatorTask.is_on_pi() and not CommunicatorTask.is_network_module_connected()

    def __open_interface(self):
        if self.__is_modi_pi(): 
            return

        self.__task.open_conn()

    def run(self):
        self.__open_interface()

        read_thread = th.Thread(
            target=self.__task.run_read_data, args=(self.__delay,)
        )
        read_thread.daemon = True
        read_thread.start()

        write_thread = th.Thread(
            target=self.__task.run_write_data, args=(self.__delay,)
        )
        write_thread.daemon = True
        write_thread.start()

        read_thread.join()
        write_thread.join()
