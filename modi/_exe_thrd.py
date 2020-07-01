import threading as th

from modi.task.exe_task import ExeTask


class ExeThrd(th.Thread):
    """
    :param send_q: Inter-process queue for serial writing message
    :param recv_q: Inter-process queue for receiving json message
    :param dict() module_ids: dict() of module_id : ['timestamp', 'uuid']
    :param list() modules: list() of module instance
    """

    def __init__(self, modules, module_ids, topology_data,
                 recv_q, send_q, init_event, nb_modules, firmware_updater,
                 init_flag):
        super().__init__()
        self.__exe_task = ExeTask(
            modules, module_ids, topology_data, recv_q, send_q,
            init_event, nb_modules, firmware_updater,
        )
        self.__init_flag = init_flag

    def request_topology(self):
        self.__exe_task.request_topology()

    def reboot(self):
        self.__exe_task.reboot()

    def run(self) -> None:
        """ Run executor task

        :return: None
        """
        self.__init_flag.set()
        while True:
            self.__exe_task.run(delay=0.001)
