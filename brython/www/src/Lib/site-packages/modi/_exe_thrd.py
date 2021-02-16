import threading as th

from modi.task.exe_task import ExeTask


class ExeThrd(th.Thread):
    """
    :param list() modules: list() of module instance
    """

    def __init__(self, modules, topology_data, conn_task):
        super().__init__(daemon=True)
        conn_task.open_conn()
        self.__exe_task = ExeTask(
            modules, topology_data, conn_task
        )
        self.__kill_sig = False

    def close(self):
        self.__kill_sig = True

    def run(self) -> None:
        """ Run executor task

        :return: None
        """
        while True:
            self.__exe_task.run(delay=0.001)
            if self.__kill_sig:
                break
