"""Main MODI module."""

import atexit
import time
from importlib import import_module as im

from modi._exe_thrd import ExeThrd
from modi.util.misc import module_list
from modi.util.topology_manager import TopologyManager


class MODI:

    def __init__(self, conn_mode="ser", verbose=False, port=None):
        # TODO: Fix OR logic here
        #if conn_mode and (conn_mode != "ser" or conn_mode != "vir"):
        #    raise ValueError("Custom conn_mode is not supported in demo!")
        if port:
            print("Cannot set port in demo version!")
            raise ValueError("Custom port is not supported in demo version!")

        self._modules = list()
        self._topology_data = dict()

        self._conn = self.__init_task(conn_mode, verbose)

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
        print("MODI modules are initialized!")
        atexit.register(self.close)

    @staticmethod
    def __init_task(conn_mode, verbose):
        if conn_mode == "ser":
            return im('modi.task.ser_task').SerTask(verbose)
        else:
            return im('modi.task.vir_task').VirTask(verbose)

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
        self._conn.send_nowait(message)

    def recv(self):
        return self._conn.recv()

    def print_topology_map(self, print_id):
        self._topology_manager.print_topology_map(print_id)

    @property
    def modules(self):
        return module_list(self._modules)

    @property
    def networks(self):
        return module_list(self._modules, 'network')

    @property
    def buttons(self):
        return module_list(self._modules, 'button')

    @property
    def dials(self):
        return module_list(self._modules, "dial")

    @property
    def displays(self):
        return module_list(self._modules, "display")

    @property
    def envs(self):
        return module_list(self._modules, "env")

    @property
    def gyros(self):
        return module_list(self._modules, "gyro")

    @property
    def irs(self):
        return module_list(self._modules, "ir")

    @property
    def leds(self):
        return module_list(self._modules, "led")

    @property
    def mics(self):
        return module_list(self._modules, "mic")

    @property
    def motors(self):
        return module_list(self._modules, "motor")

    @property
    def speakers(self):
        return module_list(self._modules, "speaker")

    @property
    def ultrasonics(self):
        return module_list(self._modules, "ultrasonic")
