import os
import traceback
from abc import ABC
from abc import abstractmethod
from typing import List

import serial.tools.list_ports as stl
from serial.tools.list_ports_common import ListPortInfo


class MODIConnectionError(Exception):
    pass


class ConnTask(ABC):

    def __init__(self, recv_q, send_q):
        self._recv_q = recv_q
        self._send_q = send_q

    @staticmethod
    def list_modi_ports() -> List[ListPortInfo]:
        """Returns a list of connected MODI ports

        :return: List[ListPortInfo]
        """
        def __is_modi_port(port):
            return (
                port.manufacturer == "LUXROBO"
                or port.product == "MODI Network Module"
                or port.description == "MODI Network Module"
                or (port.vid == 12254 and port.pid == 2))

        return [port for port in stl.comports() if __is_modi_port(port)]

    @staticmethod
    def is_on_pi() -> bool:
        """Returns whether connected to pi

        :return: true if connected to pi
        :rtype: bool
        """
        return os.name != "nt" and os.uname()[4][:3] == "arm"

    @staticmethod
    def is_network_module_connected() -> bool:
        """Returns whether network module is connected

        :return: true if connected
        :rtype: bool
        """
        return bool(ConnTask.list_modi_ports())

    #
    # Abstract Methods
    #
    @abstractmethod
    def _close_conn(self):
        pass

    @abstractmethod
    def _recv_data(self):
        pass

    @abstractmethod
    def _send_data(self):
        pass

    @abstractmethod
    def open_conn(self):
        pass

    def run_recv_data(self, delay: float):
        while True:
            try:
                self._recv_data()
            except MODIConnectionError:
                print("\nMODI connection is lost!!!")
                traceback.print_exc()
                os._exit(1)

    def run_send_data(self, delay: float):
        while True:
            try:
                self._send_data()
            except MODIConnectionError:
                print("\nMODI connection is lost!!!")
                traceback.print_exc()
                os._exit(1)
