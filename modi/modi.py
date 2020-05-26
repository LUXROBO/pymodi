"""Main MODI module."""

import time

import threading as th
import multiprocessing as mp

import threading

import networkx as nx

from pprint import pprint

from modi._communicator import Communicator
from modi._executor_thread import ExecutorThread
from modi._firmware_updater import FirmwareUpdater


class MODI:
    """
    Example:
    >>> import modi
    >>> bundle = modi.MODI()
    """

    def __init__(self, nb_modules, test=False):
        self._modules = list()
        self._module_ids = dict()
        self._topology_data = dict()

        self._recv_q = mp.Queue()
        self._send_q = mp.Queue()

        self._com_proc = None
        self._exe_thrd = None

        # Init flag used to notify initialization of MODI modules
        self._init_event = threading.Event()

        # Init number of the connected modi modules
        self._nb_modules = nb_modules

        self.firmware_updater = FirmwareUpdater(self._send_q, self._module_ids)

        if test: return

        self._com_proc = Communicator(self._recv_q, self._send_q)
        self._com_proc.daemon = True
        self._com_proc.start()
        time.sleep(1)

        self._exe_thrd = ExecutorThread(
            self._modules,
            self._module_ids,
            self._topology_data,
            self._recv_q,
            self._send_q,
            self._init_event,
            self._nb_modules,
            self.firmware_updater,
        )
        self._exe_thrd.daemon = True
        self._exe_thrd.start()
        time.sleep(1)

        self._init_event.wait()
        print("MODI modules are initialized!")

    def update_module_firmware(self):
        """Updates firmware of connected modules"""
        print("Request to update firmware of connected MODI modules.")
        self.firmware_updater.reset_state()
        self.firmware_updater.request_to_update_firmware()
        #self.firmware_updater.update_event.wait()
        print("Module firmwares have been updated!")

    def print_ids(self):
        for module in self.modules:
            pprint('module: {}, module_id: {}'.format(module, module.id))

    def print_topology_map(self):
        # start_time = time.time()
        tp_data = self._topology_data
        graph = nx.Graph()

        # Init graph nodes
        labels = {}
        for module_id in tp_data:
            curr_module_tp_data = tp_data[module_id]
            module_type = self.__get_type_from_uuid(
                curr_module_tp_data['uuid']
            )
            labels[module_id] = module_type
            graph.add_node(module_id)
        # print('graph.nodes():', graph.nodes())

        # Init graph edges
        for module_id in tp_data:
            curr_edges = []
            curr_module_tp_data = tp_data[module_id]

            # Check if module exists at R (Right) T (Top) L (Left) B (Bottom)
            if curr_module_tp_data['r'] is not None:
                edge_to_right = (module_id, curr_module_tp_data['r'])
                curr_edges.append(edge_to_right)
            if curr_module_tp_data['t'] is not None:
                edge_to_top = (module_id, curr_module_tp_data['t'])
                curr_edges.append(edge_to_top)
            if curr_module_tp_data['l'] is not None:
                edge_to_left = (module_id, curr_module_tp_data['l'])
                curr_edges.append(edge_to_left)
            if curr_module_tp_data['b'] is not None:
                edge_to_bottom = (module_id, curr_module_tp_data['b'])
                curr_edges.append(edge_to_bottom)

            graph.add_edges_from(curr_edges)
        # print('graph.edges():', graph.edges())

        labeled_graph = nx.relabel_nodes(graph, labels)
        # print('total time taken:', time.time() - start_time)

        return labeled_graph

    def __get_type_from_uuid(self, uuid):
        if uuid is None:
            return 'Network'

        hexadecimal = hex(uuid).lstrip("0x")
        type_indicator = str(hexadecimal)[:4]
        module_type = {
            # Input modules
            '2000': 'Env',
            '2010': 'Gyro',
            '2020': 'Mic',
            '2030': 'Button',
            '2040': 'Dial',
            '2050': 'Ultrasonic',
            '2060': 'Infrared',

            # Output modules
            '4000': 'Display',
            '4010': 'Motor',
            '4020': 'Led',
            '4030': 'Speaker',
        }.get(type_indicator)
        return module_type

    @property
    def modules(self):
        """Tuple of connected modules except network module.
        Example:
        >>> bundle = modi.MODI()
        >>> modules = bundle.modules
        """

        return tuple(self._modules)

    @property
    def buttons(self):
        """Tuple of connected :class:`~modi.module.button.Button` modules.
        """

        return tuple([module for module in self.modules
                      if module.type == "button"])

    @property
    def dials(self):
        """Tuple of connected :class:`~modi.module.dial.Dial` modules.
        """

        return tuple([module for module in self.modules
                      if module.type == "dial"])

    @property
    def displays(self):
        """Tuple of connected :class:`~modi.module.display.Display` modules.
        """

        return tuple([module for module in self.modules
                      if module.type == "display"])

    @property
    def envs(self):
        """Tuple of connected :class:`~modi.module.env.Env` modules.
        """

        return tuple([module for module in self.modules
                      if module.type == "env"])

    @property
    def gyros(self):
        """Tuple of connected :class:`~modi.module.gyro.Gyro` modules.
        """

        return tuple([module for module in self.modules
                      if module.type == "gyro"])

    @property
    def irs(self):
        """Tuple of connected :class:`~modi.module.ir.Ir` modules.
        """

        return tuple([module for module in self.modules
                      if module.type == "ir"])

    @property
    def leds(self):
        """Tuple of connected :class:`~modi.module.led.Led` modules.
        """

        return tuple([module for module in self.modules
                      if module.type == "led"])

    @property
    def mics(self):
        """Tuple of connected :class:`~modi.module.mic.Mic` modules.
        """

        return tuple([module for module in self.modules
                      if module.type == "mic"])

    @property
    def motors(self):
        """Tuple of connected :class:`~modi.module.motor.Motor` modules.
        """

        return tuple([module for module in self.modules
                      if module.type == "motor"])

    @property
    def speakers(self):
        """Tuple of connected :class:`~modi.module.speaker.Speaker` modules.
        """

        return tuple([module for module in self.modules
                      if module.type == "speaker"])

    @property
    def ultrasonics(self):
        """Tuple of connected :class:`~modi.module.ultrasonic.Ultrasonic` modules.
        """

        return tuple([module for module in self.modules
                      if module.type == "ultrasonic"])
