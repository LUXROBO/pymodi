
import os
import threading as th
import multiprocessing as mp
import serial.tools.list_ports as stl

from modi._communicator_task import CommunicatorTask
from modi._ser_task import SerTask
from modi._can_task import CanTask


class Communicator(mp.Process):
    """
    :param queue read_q: Multiprocessing Queue for reading raw data
    :param queue write_q: Multiprocessing Queue for writing raw data
    """

    def __init__(self, read_q, write_q):
        super(Communicator, self).__init__()
        
        # modi_ports = self._list_modi_ports()

        self.__task = CanTask(read_q, write_q) if (
            self.is_on_pi() and
            not self.is_network_module_connected()) \
            else SerTask(read_q, write_q)
        self.__delay = 0.001

    # def _list_modi_ports(self):
    #     def __is_modi_port(port):
    #         return (
    #             port.manufacturer == "LUXROBO" or
    #             port.product == "MODI Network Module" or
    #             port.description == "MODI Network Module" or
    #             (port.vid == 12254 and port.pid == 2)
    #         )

    #     return [port for port in stl.comports() if __is_modi_port(port)]

    def is_on_pi(self):
        return os.name != 'nt' and os.uname()[4][:3] == "arm"

    def is_network_module_connected(self):
        # return bool(self._list_modi_ports())
        return True

    def run(self):
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
