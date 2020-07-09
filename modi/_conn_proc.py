
import threading as th
import multiprocessing as mp

from modi.task.conn_task import ConnTask
from modi.task.ser_task import SerTask
from modi.task.can_task import CanTask
from modi.task.spp_task import SppTask
from modi.util.conn_util import is_modi_pi


class ConnProc(mp.Process):

    def __init__(self, recv_q, send_q, conn_mode, module_uuid, verbose,
                 init_flag, port=None):
        super().__init__()
        params = [recv_q, send_q, verbose]
        if conn_mode.startswith("b"):
            params.append(module_uuid)
        if conn_mode.startswith('s'):
            params.append(port)
        self.__task = self.__init_task(conn_mode)(*params)
        self.__delay = 0.05 if isinstance(self.__task, SppTask) else 0.001
        self.__init_flag = init_flag

    def __init_task(self, conn_mode: str) -> ConnTask:
        """Initialize task with given connection mode

        :param conn_mode: Desired connection mode
        :type conn_mode: str
        :return: Corresponding connection task
        :rtype: ConnTask
        """
        if conn_mode.startswith("b"):
            return SppTask
        return CanTask if is_modi_pi() else SerTask

    def run(self) -> None:
        """Run the connection

        :return: None
        """
        self.__task.open_conn()

        recv_thread = th.Thread(
            target=self.__task.run_recv_data, args=(self.__delay,)
        )
        recv_thread.daemon = True
        recv_thread.start()

        send_thread = th.Thread(
            target=self.__task.run_send_data, args=(self.__delay,)
        )
        send_thread.daemon = True
        send_thread.start()

        self.__init_flag.set()

        recv_thread.join()
        send_thread.join()
