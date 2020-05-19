"""Main MODI module."""

import time

import threading as th
import multiprocessing as mp

import networkx as nx

from pprint import pprint

from modi._communicator import Communicator
from modi._executor_thread import ExecutorThread

from modi.module.input_module.button import Button
from modi.module.input_module.dial import Dial
from modi.module.input_module.env import Env
from modi.module.input_module.gyro import Gyro
from modi.module.input_module.ir import Ir
from modi.module.input_module.mic import Mic
from modi.module.input_module.ultrasonic import Ultrasonic

from modi.module.output_module.display import Display
from modi.module.output_module.led import Led
from modi.module.output_module.motor import Motor
from modi.module.output_module.speaker import Speaker


class MODI:
    """
    Example:
    >>> import modi
    >>> bundle = modi.MODI()
    """

    def __init__(self, nb_modules, conn_mode="serial", module_uuid="", test=False):
        self._modules = list()
        self._module_ids = dict()
        self._topology_data = dict()

        self._recv_q = mp.Queue()
        self._send_q = mp.Queue()

        self._com_proc = None
        self._exe_thrd = None

        # Init flag used to notify initialization of MODI modules
        module_init_flag = th.Event()

        # If in test run, do not create process and thread
        if test:
            return

        self._com_proc = Communicator(
            self._recv_q, self._send_q, conn_mode, module_uuid
        )
        self._com_proc.daemon = True
        self._com_proc.start()
        time.sleep(1)

        self._exe_thrd = ExecutorThread(
            self._modules,
            self._module_ids,
            self._topology_data,
            self._recv_q,
            self._send_q,
            module_init_flag,
            nb_modules,
        )
        self._exe_thrd.daemon = True
        self._exe_thrd.start()
        time.sleep(1)

        module_init_timeout = 10 if conn_mode.startswith("ser") else 25
        module_init_flag.wait(timeout=module_init_timeout)
        if not module_init_flag.is_set():
            raise Exception("Modules are not initialized properly!")
        print("MODI modules are initialized!")

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
                      if isinstance(module, Button)])

    @property
    def dials(self):
        """Tuple of connected :class:`~modi.module.dial.Dial` modules.
        """

        return tuple([module for module in self.modules
                      if isinstance(module, Dial)])

    @property
    def displays(self):
        """Tuple of connected :class:`~modi.module.display.Display` modules.
        """

        return tuple([module for module in self.modules
                      if isinstance(module, Display)])

    @property
    def envs(self):
        """Tuple of connected :class:`~modi.module.env.Env` modules.
        """

        return tuple([module for module in self.modules
                      if isinstance(module, Env)])

    @property
    def gyros(self):
        """Tuple of connected :class:`~modi.module.gyro.Gyro` modules.
        """

        return tuple([module for module in self.modules
                      if isinstance(module, Gyro)])

    @property
    def irs(self):
        """Tuple of connected :class:`~modi.module.ir.Ir` modules.
        """

        return tuple([module for module in self.modules
                      if isinstance(module, Ir)])

    @property
    def leds(self):
        """Tuple of connected :class:`~modi.module.led.Led` modules.
        """

        return tuple([module for module in self.modules
                      if isinstance(module, Led)])

    @property
    def mics(self):
        """Tuple of connected :class:`~modi.module.mic.Mic` modules.
        """

        return tuple([module for module in self.modules
                      if isinstance(module, Mic)])

    @property
    def motors(self):
        """Tuple of connected :class:`~modi.module.motor.Motor` modules.
        """

        return tuple([module for module in self.modules
                      if isinstance(module, Motor)])

    @property
    def speakers(self):
        """Tuple of connected :class:`~modi.module.speaker.Speaker` modules.
        """

        return tuple([module for module in self.modules
                      if isinstance(module, Speaker)])

    @property
    def ultrasonics(self):
        """Tuple of connected :class:`~modi.module.ultrasonic.Ultrasonic` modules.
        """

        return tuple([module for module in self.modules
                      if isinstance(module, Ultrasonic)])
