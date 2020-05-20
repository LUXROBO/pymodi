
import threading as th
import multiprocessing as mp

from modi.task.conn_task import ConnTask
from modi.task.ser_task import SerTask
from modi.task.can_task import CanTask
from modi.task.spp_task import SppTask


class ConnProc(mp.Process):

    def __init__(self, recv_q, send_q, conn_mode, module_uuid):
        super().__init__()
        params = [recv_q, send_q]
        if conn_mode.startswith("b"):
            params.append(module_uuid)
        self.__task = self.__init_task(conn_mode)(*params)
        self.__delay = 0.05 if isinstance(self.__task, SppTask) else 0.001

    def __init_task(self, conn_mode: str) -> ConnTask:
        if conn_mode.startswith("b"):
            return SppTask
        return CanTask if self.__is_modi_pi() else SerTask

    @staticmethod
    def __is_modi_pi() -> bool:
        return ConnTask.is_on_pi() and \
               not ConnTask.is_network_module_connected()

    def run(self) -> None:
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
