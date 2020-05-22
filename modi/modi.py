"""Main MODI module."""

import time
from typing import Tuple

import threading as th
import multiprocessing as mp

import networkx as nx

from pprint import pprint

from modi._conn_proc import ConnProc
from modi._exe_thrd import ExeThrd

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

    def __init__(self, nb_modules: int, conn_mode: str = "serial", module_uuid: str = "", test: bool = False):
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

        self._com_proc = ConnProc(
            self._recv_q, self._send_q, conn_mode, module_uuid
        )
        self._com_proc.daemon = True
        self._com_proc.start()
        time.sleep(1)

        self._exe_thrd = ExeThrd(
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

    def print_ids(self) -> None:
        """Print all module ids

        :return: None
        """
        for module in self.modules:
            pprint('module: {}, module_id: {}'.format(module, module.id))

    def print_topology_map(self) -> None:
        """Print topology map

        :return: None
        """
        class Tree:
            def __init__(self, module_id):
                self.connected_modules = []
                self.id = module_id

            def make_tree(self, so_far, data):
                directions = ['t', 'b', 'l', 'r']
                module_data = data[self.id]
                for direction in directions:
                    conn_id = module_data[direction]
                    if conn_id not in so_far and conn_id is not None:
                        so_far.append(conn_id)
                        child = Tree(conn_id)
                        child.make_tree(so_far, data)
                        self.connected_modules.append(child)

        def print_tree(tree, depth):
            name = self.__get_type_from_uuid(tp_data[tree.id]['uuid'])
            s = name
            depth += len(name)
            for i in range(len(tree.connected_modules)):
                if i is not 0:
                    s += " " * depth
                s += " - " + print_tree(tree.connected_modules[i], depth+3)
            if len(tree.connected_modules) is 0:
                s += "\n"
            return s

        tp_data = self._topology_data
        init_id = list(tp_data.keys())[0]
        tp_tree = Tree(init_id)
        tp_tree.make_tree([init_id], tp_data)
        print("\n<<MODI Topology Map>>")
        print("Ex) ModuleA -ModuleB "+'\n'+"            -ModuleC")
        print("means that ModuleB and ModuleC are connected to ModuleA.")

        print("-" * 60)
        print(print_tree(tp_tree, 0), end='')

    def print_topology_matrix(self) -> None:
        """Print the topology map

        :return: None
        """
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

        graph = nx.relabel_nodes(graph, labels)
        matrix = nx.adjacency_matrix(graph).todense().tolist()
        nodes = list(graph)
        table_length = 13 * (len(nodes) + 1) - 2

        title = "<<Topology Adjacency Matrix>>"
        result = "\n" + " " * ((table_length - len(title)) // 2) + title + "\n"
        result += "=" * table_length + "\n" + " " * 10 + "| "
        for node in nodes:
            result += "{0:<10} | ".format(node)
        result += '\n' + '-' * table_length + '\n'
        for i in range(len(nodes)):
            result += "{0:<10}| ".format(nodes[i])
            for elem in matrix[i]:
                result += "{0:<10} | ".format(elem)
            result += '\n'
        print(result)
        # print('graph.edges():', graph.edges())
        #labeled_graph = nx.relabel_nodes(graph, labels)
        # print('total time taken:', time.time() - start_time)
        #return labeled_graph

    def __get_type_from_uuid(self, uuid: int) -> str:
        """Returns type based on uuid

        :param uuid: UUID of the required type
        :type uuid: int
        :return: Corresponding type
        :rtype: str
        """
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
