"""Main MODI module."""

import time
from typing import Optional

from modi._exe_thrd import ExeThrd
from modi.util.conn_util import is_on_pi
from modi.util.misc import module_list
from modi.util.stranger import check_complete
from modi.util.topology_manager import TopologyManager
from modi.firmware_updater import STM32FirmwareUpdater, ESP32FirmwareUpdater


class MODI:

    def __init__(self, conn_mode: str = "", verbose: bool = False,
                 port: str = None):
        self._modules = list()
        self._topology_data = dict()

        self._conn = self.__init_task(conn_mode, verbose, port)

        self._exe_thrd = ExeThrd(
            self._modules, self._topology_data, self._conn
        )
        self._exe_thrd.start()

        self._topology_manager = TopologyManager(self._topology_data,
                                                 self._modules)

        init_time = time.time()
        while not self._topology_manager.is_topology_complete():
            time.sleep(0.1)
            if time.time() - init_time > 5:
                print("MODI init timeout over. "
                      "Check your module connection.")
                break
        check_complete(self)
        print("MODI modules are initialized!")

    @staticmethod
    def __init_task(conn_mode, verbose, port):
        if not conn_mode:
            conn_mode = 'can' if is_on_pi() else 'ser'

        if conn_mode == 'ser':
            from modi.task.ser_task import SerTask
            return SerTask(verbose, port)
        elif conn_mode == 'can':
            from modi.task.can_task import CanTask
            return CanTask(verbose)
        else:
            raise ValueError(f'Invalid conn mode {conn_mode}')

    def send(self, message) -> None:
        """Low level method to send json pkt directly to modules

        :param message: Json packet to send
        :return: None
        """
        self._conn.send(message)

    def recv(self) -> Optional[str]:
        """Low level method to receive json pkt directly from modules

        :return: Json msg received
        :rtype: str if msg exists, else None
        """
        return self._conn.recv()

    def print_topology_map(self, print_id: bool = False) -> None:
        """Prints out the topology map

        :param print_id: if True, the result includes module id
        :return: None
        """
        self._topology_manager.print_topology_map(print_id)

    @property
    def modules(self) -> module_list:
        """Module List of connected modules except network module.
        """
        return module_list(
            list(filter(lambda module: module.module_type != 'Network',
                        self._modules))
        )

    @property
    def buttons(self) -> module_list:
        """Module List of connected Button modules.
        """
        return module_list(self._modules, 'button')

    @property
    def dials(self) -> module_list:
        """Module List of connected Dial modules.
        """
        return module_list(self._modules, "dial")

    @property
    def displays(self) -> module_list:
        """Module List of connected Display modules.
        """
        return module_list(self._modules, "display")

    @property
    def envs(self) -> module_list:
        """Module List of connected Env modules.
        """
        return module_list(self._modules, "env")

    @property
    def gyros(self) -> module_list:
        """Module List of connected Gyro modules.
        """
        return module_list(self._modules, "gyro")

    @property
    def irs(self) -> module_list:
        """Module List of connected Ir modules.
        """
        return module_list(self._modules, "ir")

    @property
    def leds(self) -> module_list:
        """Module List of connected Led modules.
        """
        return module_list(self._modules, "led")

    @property
    def mics(self) -> module_list:
        """Module List of connected Mic modules.
        """
        return module_list(self._modules, "mic")

    @property
    def motors(self) -> module_list:
        """Module List of connected Motor modules.
        """
        return module_list(self._modules, "motor")

    @property
    def speakers(self) -> module_list:
        """Module List of connected Speaker modules.
        """
        return module_list(self._modules, "speaker")

    @property
    def ultrasonics(self) -> module_list:
        """Module List of connected Ultrasonic modules.
        """
        return module_list(self._modules, "ultrasonic")


def update_module_firmware():
    updater = STM32FirmwareUpdater()
    updater.update_module_firmware()


def update_network_firmware(stub=True, force=False):
    updater = ESP32FirmwareUpdater()
    updater.start_update(stub=stub, force=force)
