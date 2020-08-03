import threading as th

from modi.task.exe_task import ExeTask


class ExeThrd(th.Thread):
    """
    :param send_q: Inter-process queue for serial writing message
    :param recv_q: Inter-process queue for receiving json message
    :param dict() module_ids: dict() of module_id : ['timestamp', 'uuid']
    :param list() modules: list() of module instance
    """

    def __init__(self, modules, topology_data, recv_q, send_q):
        super().__init__(daemon=True)
        self.__exe_task = ExeTask(
            modules, topology_data, recv_q, send_q,
        )

    def run(self) -> None:
        """ Run executor task

        :return: None
        """
        while True:
            self.__exe_task.run(delay=0.001)
