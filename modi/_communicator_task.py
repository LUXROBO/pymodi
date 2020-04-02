
import os

import serial.tools.list_ports as stl

from abc import ABC
from abc import abstractmethod


class CommunicatorTask(ABC):

    def __init__(self, recv_q, send_q):
        self._recv_q = recv_q
        self._send_q = send_q

    @staticmethod
    def _list_modi_ports():
        def __is_modi_port(port):
            return (
                port.manufacturer == "LUXROBO" or
                port.product == "MODI Network Module" or
                port.description == "MODI Network Module" or
                (port.vid == 12254 and port.pid == 2)
            )

        return [port for port in stl.comports() if __is_modi_port(port)]

    @staticmethod
    def is_on_pi():
        return os.name != "nt" and os.uname()[4][:3] == "arm"

    @staticmethod
    def is_network_module_connected():
        return bool(CommunicatorTask._list_modi_ports())

    #
    # Abstract Methods
    #
    @abstractmethod
    def _close_conn(self):
        pass

    @abstractmethod
    def _read_data(self):
        pass

    @abstractmethod
    def _write_data(self):
        pass

    @abstractmethod
    def open_conn(self):
        pass

    @abstractmethod
    def run_read_data(self, delay):
        pass

    @abstractmethod
    def run_write_data(self, delay):
        pass
