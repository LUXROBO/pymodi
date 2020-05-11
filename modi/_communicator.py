
import threading as th
import multiprocessing as mp

from modi._communicator_task import CommunicatorTask
from modi._ser_task import SerTask
from modi._can_task import CanTask
from modi._spp_task import SppTask


class Communicator(mp.Process):

    def __init__(self, recv_q, send_q, conn_mode):
        super().__init__()
        self.__task = self.__init_task(conn_mode)(recv_q, send_q)
        self.__delay = 0.01

    def __init_task(self, conn_mode):
        if conn_mode.startswith("bluetooth") or conn_mode.startswith("spp"):
            return SppTask
        if self.__is_modi_pi():
            return CanTask
        return SerTask

    @staticmethod
    def __is_modi_pi():
        return CommunicatorTask.is_on_pi() and not CommunicatorTask.is_network_module_connected()

    def run(self):
        self.__task.open_conn()

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
