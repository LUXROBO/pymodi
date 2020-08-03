
import threading as th
import multiprocessing as mp

from modi.task.conn_task import ConnTask
from modi.task.ser_task import SerTask
from modi.task.can_task import CanTask
from modi.task.spp_task import SppTask


class ConnProc(mp.Process):

    def __init__(self, recv_q, send_q, conn_mode, module_uuid, verbose,
                 port=None):
        super().__init__(daemon=True)
        params = [recv_q, send_q, verbose]
        if conn_mode.startswith("b"):
            params.append(module_uuid)
        if conn_mode.startswith('s'):
            params.append(port)
        self.__task = self.__init_task(conn_mode)(*params)
        self.__delay = 0.05 if isinstance(self.__task, SppTask) else 0.001

    def __init_task(self, conn_mode: str) -> ConnTask:
        """Initialize task with given connection mode

        :param conn_mode: Desired connection mode
        :type conn_mode: str
        :return: Corresponding connection task
        :rtype: ConnTask
        """
        if conn_mode == 'spp':
            return SppTask
        elif conn_mode == 'can':
            return CanTask
        elif conn_mode == 'ser':
            return SerTask
        else:
            return CanTask if self.__is_modi_pi() else SerTask

    @staticmethod
    def __is_modi_pi() -> bool:
        """Returns whether connection is on pi

        :return: true is on pi
        :rtype: bool
        """
        return ConnTask.is_on_pi() and \
            not ConnTask.is_network_module_connected()

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

        recv_thread.join()
        send_thread.join()
