import threading as th

from modi.task.exe_task import ExeTask


class ExeThrd(th.Thread):
    """
    :param queue send_q: Inter-process queue for serial writing message
    :param queue recv_q: Inter-process queue for receiving json message
    :param dict() module_ids: dict() of module_id : ['timestamp', 'uuid']
    :param list() modules: list() of module instance
    """

    def __init__(self, modules, module_ids, topology_data,
                 recv_q, send_q, init_event, nb_modules):
        super().__init__()
        self.__exe_task = ExeTask(
            modules, module_ids, topology_data, recv_q, send_q,
            init_event, nb_modules
        )

    def run(self) -> None:
        """ Run executor task

        :return: None
        """

        while True:
            self.__exe_task.run(delay=0.001)
