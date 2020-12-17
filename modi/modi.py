"""Main MODI module."""

import sys
import time
import atexit
import logging

from importlib import import_module as im

from modi._exe_thrd import ExeThrd
from modi.util.connection_util import is_network_module_connected, is_on_pi
from modi.util.miscellaneous import ModuleList
from modi.util.stranger import check_complete
from modi.util.topology_manager import TopologyManager
from modi.util.firmware_updater import STM32FirmwareUpdater
from modi.util.firmware_updater import ESP32FirmwareUpdater

from modi.about import __version__


class MODI:

    def __init__(
        self, modi_version=1, conn_type="", verbose=False, port=None,
        network_uuid="", virtual_modules=None,
    ):
        if virtual_modules and conn_type != "vir":
            raise ValueError(
                "Virtual modules can only be defined in virtual connection"
            )
        self._modules = list()
        self._topology_data = dict()

        self._conn = self.__init_task(
            conn_type, verbose, port, network_uuid,
        )

        self._exe_thrd = ExeThrd(
            self._modules, self._topology_data, self._conn
        )
        print('Start initializing connected MODI modules')
        self._exe_thrd.start()

        self._topology_manager = TopologyManager(
            self._topology_data, self._modules
        )

        init_time = time.time()
        while not self._topology_manager.is_topology_complete():
            time.sleep(0.1)
            if time.time() - init_time > 5:
                print("MODI init timeout over. "
                      "Check your module connection.")
                break
        check_complete(self)
        print("MODI modules are initialized!")

        bad_modules = (
            self.__wait_user_code_check() if conn_type != 'ble' else []
        )
        if bad_modules:
            cmd = input(f"{[str(module) for module in bad_modules]} "
                        f"has user code in it.\n"
                        f"Reset the user code? [y/n] ")
            if 'y' in cmd:
                self.close()
                modules_to_reset = filter(
                    lambda m: m.is_up_to_date, bad_modules
                )
                modules_to_update = filter(
                    lambda m: not m.is_up_to_date, bad_modules
                )
                reset_module_firmware(
                    tuple(module.id for module in modules_to_reset)
                )
                update_module_firmware(
                    tuple(module.id for module in modules_to_update)
                )
                self.open()
        atexit.register(self.close)

    def __init_logger(self):
        logger = logging.getLogger(f'PyMODI (v{__version__}) Logger')
        logger.setLevel(logging.DEBUG)

        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        file_handler = logging.FileHandler('pymodi.log')
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)

        logger.addHandler(file_handler)
        return logger

    def __wait_user_code_check(self):
        def is_not_checked(module):
            return module.user_code_status < 0

        while list(filter(is_not_checked, self._modules)):
            time.sleep(0.1)
        bad_modules = []
        for module in self._modules:
            if module.has_user_code:
                bad_modules.append(module)
        return bad_modules

    @staticmethod
    def __init_task(
        conn_type, verbose, port, network_uuid,
    ):
        if not conn_type:
            is_can = not is_network_module_connected() and is_on_pi()
            conn_type = 'can' if is_can else 'ser'

        if conn_type == 'ser':
            return im('modi.task.ser_task').SerTask(verbose, port)
        elif conn_type == 'can':
            return im('modi.task.can_task').CanTask(verbose)
        elif conn_type == 'vir':
            return im('modi.task.vir_task').VirTask(verbose, port)
        elif conn_type == 'ble':
            mod_path = {
                'win32': 'modi.task.ble_task.ble_task_win',
                'linux': 'modi.task.ble_task.ble_task_rpi',
                'darwin': 'modi.task.ble_task.ble_task_mac',
            }.get(sys.platform)
            return im(mod_path).BleTask(verbose, network_uuid)
        else:
            raise ValueError(f'Invalid conn mode {conn_type}')

    def open(self):
        atexit.register(self.close)
        self._exe_thrd = ExeThrd(
            self._modules, self._topology_data, self._conn
        )
        self._conn.open_conn()
        self._exe_thrd.start()

    def close(self):
        atexit.unregister(self.close)
        print("Closing MODI connection...")
        self._exe_thrd.close()
        self._conn.close_conn()

    def send(self, message):
        """Low level method to send json pkt directly to modules

        :param message: Json packet to send
        :return: None
        """
        self._conn.send_nowait(message)

    def recv(self):
        """Low level method to receive json pkt directly from modules

        :return: Json msg received
        :rtype: str if msg exists, else None
        """
        return self._conn.recv()

    def print_topology_map(self, print_id=False):
        """Prints out the topology map

        :param print_id: if True, the result includes module id
        :return: None
        """
        self._topology_manager.print_topology_map(print_id)

    @property
    def modules(self) -> ModuleList:
        """Module List of connected modules except network module.
        """
        return ModuleList(self._modules)

    @property
    def networks(self) -> ModuleList:
        return ModuleList(self._modules, 'network')

    @property
    def buttons(self) -> ModuleList:
        """Module List of connected Button modules.
        """
        return ModuleList(self._modules, 'button')

    @property
    def dials(self) -> ModuleList:
        """Module List of connected Dial modules.
        """
        return ModuleList(self._modules, "dial")

    @property
    def displays(self) -> ModuleList:
        """Module List of connected Display modules.
        """
        return ModuleList(self._modules, "display")

    @property
    def envs(self) -> ModuleList:
        """Module List of connected Env modules.
        """
        return ModuleList(self._modules, "env")

    @property
    def gyros(self) -> ModuleList:
        """Module List of connected Gyro modules.
        """
        return ModuleList(self._modules, "gyro")

    @property
    def irs(self) -> ModuleList:
        """Module List of connected Ir modules.
        """
        return ModuleList(self._modules, "ir")

    @property
    def leds(self) -> ModuleList:
        """Module List of connected Led modules.
        """
        return ModuleList(self._modules, "led")

    @property
    def mics(self) -> ModuleList:
        """Module List of connected Mic modules.
        """
        return ModuleList(self._modules, "mic")

    @property
    def motors(self) -> ModuleList:
        """Module List of connected Motor modules.
        """
        return ModuleList(self._modules, "motor")

    @property
    def speakers(self) -> ModuleList:
        """Module List of connected Speaker modules.
        """
        return ModuleList(self._modules, "speaker")

    @property
    def ultrasonics(self) -> ModuleList:
        """Module List of connected Ultrasonic modules.
        """
        return ModuleList(self._modules, "ultrasonic")


def update_module_firmware(target_ids=(0xFFF, )):
    updater = STM32FirmwareUpdater(target_ids=target_ids)
    updater.update_module_firmware()
    updater.close()


def reset_module_firmware(target_ids=(0xFFF, )):
    updater = STM32FirmwareUpdater(is_os_update=False, target_ids=target_ids)
    updater.update_module_firmware()
    updater.close()


def update_network_firmware(force=False):
    updater = ESP32FirmwareUpdater()
    updater.update_firmware(force=force)
