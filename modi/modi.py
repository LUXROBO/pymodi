"""Main MODI module."""

import os
import signal
import threading as th
import time
import traceback

from modi._conn_proc import ConnProc
from modi._exe_thrd import ExeThrd
from modi.util.misc import module_list
from modi.util.queues import CommunicationQueue
from modi.util.stranger import check_complete
from modi.util.topology_manager import TopologyManager
from typing import Optional


class MODI:
    # Keeps track of all the connection processes spawned
    __conn_procs = []

    def __init__(self, conn_mode: str = "serial",
                 module_uuid: str = "", test: bool = False,
                 verbose: bool = False, port: str = None):
        self._modules = list()
        self._topology_data = dict()

        self._recv_q = CommunicationQueue()
        self._send_q = CommunicationQueue()

        self._conn_proc = None
        self._exe_thrd = None
        # If in test run, do not create process and thread
        if test:
            return

        self._conn_proc = ConnProc(
            self._recv_q, self._send_q, conn_mode, module_uuid, verbose, port
        )
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

        MODI.__conn_procs.append(self._conn_proc.pid)

        self._child_watch = th.Thread(target=self.watch_child_process)
        self._child_watch.daemon = True
        self._child_watch.start()

        self._exe_thrd = ExeThrd(
            self._modules,
            self._topology_data,
            self._recv_q,
            self._send_q,
        )
        self._exe_thrd.start()

        self._topology_manager = TopologyManager(self._topology_data,
                                                 self._modules)

        while not self._topology_manager.is_topology_complete():
            time.sleep(0.1)
        check_complete(self)
        print("MODI modules are initialized!")

    def watch_child_process(self) -> None:
        """Continuously watches if any of the child processes are dead, and
        if so, terminates all the existing processes.

        :return: None
        """
        while self._conn_proc.is_alive():
            time.sleep(0.1)
        for pid in MODI.__conn_procs:
            try:
                os.kill(pid, signal.SIGTERM)
            except PermissionError:
                continue
            except ProcessLookupError:
                continue
        os.kill(os.getpid(), signal.SIGTERM)

    def send(self, message) -> None:
        """Low level method to send json pkt directly to modules

        :param message: Json packet to send
        :return: None
        """
        self._send_q.put(message)

    def recv(self) -> Optional[str]:
        """Low level method to receive json pkt directly from modules

        :return: Json msg received
        :rtype: str if msg exists, else None
        """
        if self._recv_q.empty():
            return None
        return self._recv_q.get()

    def print_topology_map(self, print_id: bool = False) -> None:
        """Prints out the topology map

        :param print_id: if True, the result includes module id
        :return: None
        """
        self._topology_manager.print_topology_map(print_id)

    @property
    def modules(self) -> module_list:
        """Tuple of connected modules except network module.
        """
        return module_list(
            list(filter(lambda module: module.module_type != 'Network',
                        self._modules))
        )

    @property
    def buttons(self) -> module_list:
        """Tuple of connected :class:`~modi.module.button.Button` modules.
        """
        return module_list(self._modules, 'button')

    @property
    def dials(self) -> module_list:
        """Tuple of connected :class:`~modi.module.dial.Dial` modules.
        """
        return module_list(self._modules, "dial")

    @property
    def displays(self) -> module_list:
        """Tuple of connected :class:`~modi.module.display.Display` modules.
        """
        return module_list(self._modules, "display")

    @property
    def envs(self) -> module_list:
        """Tuple of connected :class:`~modi.module.env.Env` modules.
        """
        return module_list(self._modules, "env")

    @property
    def gyros(self) -> module_list:
        """Tuple of connected :class:`~modi.module.gyro.Gyro` modules.
        """
        return module_list(self._modules, "gyro")

    @property
    def irs(self) -> module_list:
        """Tuple of connected :class:`~modi.module.ir.Ir` modules.
        """
        return module_list(self._modules, "ir")

    @property
    def leds(self) -> module_list:
        """Tuple of connected :class:`~modi.module.led.Led` modules.
        """
        return module_list(self._modules, "led")

    @property
    def mics(self) -> module_list:
        """Tuple of connected :class:`~modi.module.mic.Mic` modules.
        """
        return module_list(self._modules, "mic")

    @property
    def motors(self) -> module_list:
        """Tuple of connected :class:`~modi.module.motor.Motor` modules.
        """
        return module_list(self._modules, "motor")

    @property
    def speakers(self) -> module_list:
        """Tuple of connected :class:`~modi.module.speaker.Speaker` modules.
        """
        return module_list(self._modules, "speaker")

    @property
    def ultrasonics(self) -> module_list:
        """Tuple of connected :class:`~modi.module.ultrasonic.Ultrasonic`
        modules.
        """
        return module_list(self._modules, "ultrasonic")
