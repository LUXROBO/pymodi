
import time
import threading as th
import multiprocessing as mp

from modi._communicator_task import CommunicatorTask
from modi._ser_task import SerTask
from modi._can_task import CanTask
from modi._ble_task import BleTask

class Communicator(mp.Process):

    def __init__(self, recv_q, send_q):
        super().__init__()
        #self.__task = CanTask(recv_q, send_q) if self.__is_modi_pi() else SerTask(recv_q, send_q)
        self.__task = BleTask(recv_q, send_q)
        self.__delay = 0.001

    def __is_modi_pi(self):
        return CommunicatorTask.is_on_pi() and not CommunicatorTask.is_network_module_connected()

    def run(self):
        #self.__task.open_conn()

        #read_thread = th.Thread(
        #    target=self.__task.run_read_data, args=(self.__delay,)
        #)
        #read_thread.daemon = True
        #read_thread.start()

        #write_thread = th.Thread(
        #    target=self.__task.run_write_data, args=(self.__delay,)
        #)
        #write_thread.daemon = True
        #write_thread.start()

        #read_thread.join()
        #write_thread.join()
        self.__task.ble_up()
        self.__task.connect('MODI_996DC5B0')
        self.__task.subscribe('00008421-0000-1000-8000-00805F9B34FB')
        
        while True:
            time.sleep(0.01)
