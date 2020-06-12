"""Main MODI module."""

import os
import time
import traceback

import threading as th
import multiprocessing as mp

from typing import Tuple

from modi._conn_proc import ConnProc
from modi._exe_thrd import ExeThrd

from modi.module.module import Module
from modi.module.ai_module import AI_camera, AI_mic, AI_speaker

from modi.util.topology_manager import TopologyManager
from modi.util.firmware_updater import FirmwareUpdater
from modi.util.that import check_complete



class MODI:
    """
    Example:
    >>> import modi
    >>> bundle = modi.MODI()
    """

    def __init__(self, nb_modules: int, conn_mode: str = "serial",
                 module_uuid: str = "", AI_mode: bool = False, test: bool = False,
                 verbose: bool = False):

        self._modules = list()
        self._module_ids = dict()
        self._AI_modules = list()
        self._topology_data = dict()

        self._recv_q = mp.Queue()
        self._send_q = mp.Queue()

        self._conn_proc = None
        self._exe_thrd = None

        # Init flag used to notify initialization of MODI modules
        module_init_flag = th.Event()

        # If in test run, do not create process and thread
        if test:
            return

        init_flag = mp.Event()

        self._conn_proc = ConnProc(
            self._recv_q, self._send_q, conn_mode, module_uuid, verbose,
            init_flag
        )
        self._conn_proc.daemon = True
        try:
            self._conn_proc.start()
        except RuntimeError:
            if os.name == 'nt':
                print('\nProcess initialization failed!\nMake sure you are '
                      'using\n    if __name__ == \'__main__\' \n '
                      'in the main module.')
            else:
                traceback.print_exc()
            exit(1)

        child_watch = th.Thread(target=self.watch_child_process)
        child_watch.daemon = True
        child_watch.start()

        init_flag.wait()

        self._firmware_updater = FirmwareUpdater(
            self._send_q, self._module_ids, nb_modules
        )

        init_flag = th.Event()

        self._exe_thrd = ExeThrd(
            self._modules,
            self._module_ids,
            self._topology_data,
            self._recv_q,
            self._send_q,
            module_init_flag,
            nb_modules,
            self._firmware_updater,
            init_flag
        )
        self._exe_thrd.daemon = True
        self._exe_thrd.start()

        init_flag.wait()

        self._topology_manager = TopologyManager(self._topology_data)

        module_init_flag.wait()
        if not module_init_flag.is_set():
            raise Exception("Modules are not initialized properly!")
            exit(1)
        print("MODI modules are initialized!")
        check_complete(self)

        if AI_mode:
            self._init_AI_modules()



        # if ai computing module
            # init mic -> ai_mic = AI_MIC()
            # init speaker
            # init camera

    def update_module_firmware(self) -> None:
        """Updates firmware of connected modules"""
        print("Request to update firmware of connected MODI modules.")
        self._firmware_updater.reset_state()
        self._firmware_updater.request_to_update_firmware()
        #self.firmware_updater.update_event.wait()
        print("Module firmwares have been updated!")

    def watch_child_process(self) -> None:
        while self._conn_proc.is_alive():
            time.sleep(0.1)
        os._exit(1)

    def print_topology_map(self, print_id: bool = False) -> None:
        """Prints out the topology map

        :param print_id: if True, the result includes module id
        :return: None
        """
        self._topology_manager.print_topology_map(print_id)

    #TODO : complete each method
    def _init_AI_modules(self) -> None:
        """
        """
        self._init_AI_camera()
        self._init_AI_mic()
        self._init_AI_speaker()

    def _init_AI_camera(self) -> None:
        pass

    def _init_AI_mic(self) -> None:
        pass

    def _init_AI_speaker(self) -> None:
        pass


    @property
    def modules(self) -> Tuple[Module]:
        """Tuple of connected modules except network module.
        Example:
        >>> bundle = modi.MODI()
        >>> modules = bundle.modules
        """
        return tuple(self._modules)

    @property
    def buttons(self) -> Tuple[Module]:
        """Tuple of connected :class:`~modi.module.button.Button` modules.
        """

        return tuple([module for module in self.modules
                      if module.type == "button"])

    @property
    def dials(self) -> Tuple[Module]:
        """Tuple of connected :class:`~modi.module.dial.Dial` modules.
        """

        return tuple([module for module in self.modules
                      if module.type == "dial"])

    @property
    def displays(self) -> Tuple[Module]:
        """Tuple of connected :class:`~modi.module.display.Display` modules.
        """

        return tuple([module for module in self.modules
                      if module.type == "display"])

    @property
    def envs(self) -> Tuple[Module]:
        """Tuple of connected :class:`~modi.module.env.Env` modules.
        """

        return tuple([module for module in self.modules
                      if module.type == "env"])

    @property
    def gyros(self) -> Tuple[Module]:
        """Tuple of connected :class:`~modi.module.gyro.Gyro` modules.
        """

        return tuple([module for module in self.modules
                      if module.type == "gyro"])

    @property
    def irs(self) -> Tuple[Module]:
        """Tuple of connected :class:`~modi.module.ir.Ir` modules.
        """

        return tuple([module for module in self.modules
                      if module.type == "ir"])

    @property
    def leds(self) -> Tuple[Module]:
        """Tuple of connected :class:`~modi.module.led.Led` modules.
        """

        return tuple([module for module in self.modules
                      if module.type == "led"])

    @property
    def mics(self) -> Tuple[Module]:
        """Tuple of connected :class:`~modi.module.mic.Mic` modules.
        """

        return tuple([module for module in self.modules
                      if module.type == "mic"])

    @property
    def motors(self) -> Tuple[Module]:
        """Tuple of connected :class:`~modi.module.motor.Motor` modules.
        """

        return tuple([module for module in self.modules
                      if module.type == "motor"])

    @property
    def speakers(self) -> Tuple[Module]:
        """Tuple of connected :class:`~modi.module.speaker.Speaker` modules.
        """

        return tuple([module for module in self.modules
                      if module.type == "speaker"])

    @property
    def ultrasonics(self) -> Tuple[Module]:
        """Tuple of connected :class:`~modi.module.ultrasonic.Ultrasonic` modules.
        """

        return tuple([module for module in self.modules
                      if module.type == "ultrasonic"])

    @property
    def ai_mics(self) -> Tuple[AI_mic]:
        """Tuple of connected :class:'~modi.module.ai_mic.AI_mic' modules
        """

        return tuple([ai_module for ai_module in self._AI_modules
                      if ai_module.type == "ai_mic"])

    @property
    def ai_speakers(self) -> Tuple[AI_speaker]:
        """Tuple of connected :class:'~modi.module.ai_speaker.AI_speaker' modules
        """

        return tuple([ai_module for ai_module in self._AI_modules
                      if ai_module.type == "ai_speaker"])

    def ai_cameras(self) -> Tuple[AI_camera]:
        """Tuple of connected :class:'~modi.module.ai_camera.AI_camera' modules
        """
        return tuple([ai_module for ai_module in self._AI_modules if ai_module.type == "ai_camera"])
